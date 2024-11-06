from airflow import settings
from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint, redirect, flash, url_for, request, jsonify
from flask_login import current_user
from flask_appbuilder import expose, BaseView as AppBuilderBaseView
from airflow.hooks.base import BaseHook
import pandas as pd
import re
from functools import wraps
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField, StringField, BooleanField
from wtforms.validators import Optional, DataRequired
from wtforms import ValidationError
from sqlalchemy import (
    create_engine,
    text,
    Table,
    Column,
    String,
    MetaData,
    func,
    select,
    case,
    and_,
)
from airflow.models import Variable
from sqlalchemy_redshift.dialect import RedshiftDialect_psycopg2


RedshiftDialect_psycopg2.supports_statement_cache = True


class RolePermissionForm(FlaskForm):
    role_name = StringField("Input Role")
    roles = SelectMultipleField("Select Roles", choices=[], validators=[Optional()])
    submit = SubmitField("Submit")


def validate_redshift_password(form, field):
    if not any(c.isupper() for c in field.data):
        raise ValidationError("Field must contain at least one uppercase letter.")
    if not any(c.islower() for c in field.data):
        raise ValidationError("Field must contain at least one lowercase letter.")
    if not any(c.isdigit() for c in field.data):
        raise ValidationError("Field must contain at least one digit.")


class NewUserForm(FlaskForm):
    username = StringField("Input Username", validators=[DataRequired()])
    password = StringField(
        "Input Password", validators=[DataRequired(), validate_redshift_password]
    )
    roles = SelectMultipleField("Select Roles", choices=[], validators=[Optional()])
    can_edit_database = BooleanField("Can Edit Database")
    submit = SubmitField("Submit")


class AddRolesToUser(FlaskForm):
    user_name = StringField("Input Role")
    roles = SelectMultipleField("Select Roles", choices=[], validators=[Optional()])
    submit = SubmitField("Submit")


session = settings.Session()


bp = Blueprint(
    "edw_grants",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static/edw_grants_plugin",
)


def admin_only(f):
    """Decorator to restrict access to Admin role."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "Admin" not in [role.name for role in current_user.roles]:
            flash("You do not have permission to access this page.", "danger")
            return redirect(url_for("Airflow.index"))
        return f(*args, **kwargs)

    return decorated_function


def failure_tollerant(f):
    """Decorator to restrict access to Admin role."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            flash("Something went wrong...", "danger")
            print(f"PLUGIN FAILURE: {e}")
            return redirect(url_for("EdwGrantsAppBuilderBaseView.main"))

    return decorated_function


def failure_tollerant_front_end(f):
    """Decorator to restrict access to Admin role."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            f(*args, **kwargs)
            return jsonify({"Status": "Succeeded"}), 200
        except Exception:
            flash("Something went wrong...", "danger")
            jsonify({"Status": "Failed"}), 404

    return decorated_function


class EdwGrantsAppBuilderBaseView(AppBuilderBaseView):
    default_view = "main"
    route_base = "/edw_grants"

    def __init__(self, **kwargs):
        # Pass parent_var and any other keyword arguments to the ParentClass
        super().__init__(**kwargs)
        self.metadata = MetaData()
        self.pg_user_t = Table(
            "pg_user", self.metadata, Column("usename", String), schema="pg_catalog"
        )

        self.svv_roles_t = Table(
            "SVV_ROLES", self.metadata, Column("role_name", String), schema="pg_catalog"
        )

    def sanitize_identifier(self, identifier):
        # Allow only alphanumeric characters and underscores
        if not re.match(r"^[A-Za-z0-9_]+$", identifier):
            raise ValueError(f"Invalid identifier format: {identifier}")

    def sanitize_identifiers(self, identifiers):
        # Validate each identifier in the list, raising an error if any are invalid
        for identifier in identifiers:
            self.sanitize_identifier(identifier)

    def get_edw_connection_uri(self):
        conn_name = Variable.get(
            "redshift_connection_grants_name", default_var="edw_con"
        )
        connection = BaseHook.get_connection(conn_name)
        uri = connection.get_uri()
        return uri

    def get_edw_engine(self):
        uri = self.get_edw_connection_uri()
        engine = create_engine(uri)
        return engine

    def get_edw_database(self):
        uri = self.get_edw_connection_uri()
        database_name = uri.split("/")[-1]
        return database_name

    def get_current_dbt_metadata_roles(self, engine):
        downstream = self.svv_roles_t.alias("dependent_roles")
        upstream = self.svv_roles_t.alias("roles")
        base_query = (
            select(
                downstream.c.role_name.label("role_downstream"),
                upstream.c.role_name.label("role_upstream"),
            )
            .where(
                (
                    func.role_is_member_of(downstream.c.role_name, upstream.c.role_name)
                    | (downstream.c.role_name == upstream.c.role_name)
                )
                & downstream.c.role_name.notlike("%sys:%")
            )
            .distinct()
        )
        compiled_query = base_query.compile(
            engine, compile_kwargs={"literal_binds": True}
        )
        df = pd.read_sql(str(compiled_query), con=engine)
        return df

    def get_current_dbt_metadata_users(self, engine, database_name):
        query = select(
            self.pg_user_t.c.usename.label("username"),
            self.svv_roles_t.c.role_name,
            func.has_database_privilege(
                self.pg_user_t.c.usename, database_name, "CREATE"
            ).label("can_create"),
        ).select_from(
            self.pg_user_t.outerjoin(
                self.svv_roles_t,
                func.user_is_member_of(
                    self.pg_user_t.c.usename, self.svv_roles_t.c.role_name
                ),
            )
        )
        compiled_query = query.compile(engine, compile_kwargs={"literal_binds": True})
        df = pd.read_sql(str(compiled_query), con=engine)
        return df

    def get_roles_roles_query(self, role_name, must_granted_list=[]):
        base_query = (
            select(
                [
                    self.svv_roles_t.c.role_name.label("object_name"),
                    func.role_is_member_of(
                        role_name, self.svv_roles_t.c.role_name
                    ).label("granted"),
                    case(
                        [
                            (self.svv_roles_t.c.role_name.in_(must_granted_list), True)
                        ],  # <-- Tuple (condition, result)
                        else_=False,  # Else clause for the case statement
                    ).label("must_granted"),
                ]
            )
            .where(
                and_(
                    self.svv_roles_t.c.role_name.notlike("sys%"),
                    self.svv_roles_t.c.role_name != role_name,
                )
            )
            .cte()
        )
        return base_query

    def get_users_roles_query(self, user_name, must_granted_list=[]):
        base_query = (
            select(
                [
                    self.svv_roles_t.c.role_name.label("object_name"),
                    func.user_is_member_of(
                        user_name, self.svv_roles_t.c.role_name
                    ).label("granted"),
                    case(
                        [
                            (self.svv_roles_t.c.role_name.in_(must_granted_list), True)
                        ],  # <-- Tuple (condition, result)
                        else_=False,  # Else clause for the case statement
                    ).label("must_granted"),
                ]
            )
            .where(self.svv_roles_t.c.role_name.notlike("sys%"))
            .cte()
        )
        return base_query

    def get_grant_revoke_query(self, base_query):
        final_query = select(
            [
                base_query.c.object_name,
                (base_query.c.granted != base_query.c.must_granted).label(
                    "ind_relevant"
                ),
                case(
                    [(base_query.c.must_granted == text("True"), "grant")],
                    else_="revoke",
                ).label("grant_type"),
            ]
        )
        return final_query

    def handle_roles_grants(
        self, engine, grants, object_name, grant_role_q, revoke_role_q
    ):
        self.sanitize_identifiers(
            [grant["grant_type"] for grant in grants] + [object_name]
        )
        with engine.connect() as connection:
            with connection.begin():
                for grant in grants:
                    if grant["grant_type"] == "grant":
                        connection.execute(
                            text(
                                grant_role_q.format(
                                    object_name=object_name,
                                    up_role_name=grant["object_name"],
                                )
                            )
                        )
                    else:
                        connection.execute(
                            text(
                                revoke_role_q.format(
                                    object_name=object_name,
                                    up_role_name=grant["object_name"],
                                )
                            )
                        )

    def get_roles_grants(self, engine, base_query):
        final_query = self.get_grant_revoke_query(base_query)
        compiled_query = final_query.compile(
            engine, compile_kwargs={"literal_binds": True}
        )
        df = pd.read_sql(str(compiled_query), con=engine)
        df = df[df["ind_relevant"]]
        grants = df.to_dict("records")
        return grants

    def edit_roles_roles(self, engine, role_name, must_granted_list):
        base_query = self.get_roles_roles_query(role_name, must_granted_list)
        grants = self.get_roles_grants(engine, base_query)
        grant_role_q = "grant role {up_role_name} to role {object_name}"
        revoke_role_q = "revoke role {up_role_name} from role {object_name}"
        self.handle_roles_grants(engine, grants, role_name, grant_role_q, revoke_role_q)

    def edit_users_roles(self, engine, user_name, must_granted_list):
        base_query = self.get_users_roles_query(user_name, must_granted_list)
        grants = self.get_roles_grants(engine, base_query)
        grant_role_q = "grant role {up_role_name} to {object_name}"
        revoke_role_q = "revoke role {up_role_name} from {object_name}"
        self.handle_roles_grants(engine, grants, user_name, grant_role_q, revoke_role_q)

    def get_all_roles(self, engine):
        query = select(self.svv_roles_t.c.role_name.label("role_name")).where(
            self.svv_roles_t.c.role_name.notlike("%sys:%")
        )
        compiled_query = query.compile(engine, compile_kwargs={"literal_binds": True})
        df = pd.read_sql(str(compiled_query), con=engine)
        return df

    def get_roles_dependencies(self, engine):
        df = self.get_current_dbt_metadata_roles(engine)
        df = (
            df.groupby("role_downstream")["role_upstream"]
            .agg(lambda x: list(set(x)))
            .reset_index()
        )
        df = df.sort_values(by=["role_downstream"])
        return df.to_dict("records")

    def get_users(self, engine, database_name):
        df = self.get_current_dbt_metadata_users(engine, database_name)
        df_roles = (
            df.groupby("username")["role_name"]
            .agg(lambda x: list(set(x)))
            .reset_index()
        )
        df_unique = df[["username", "can_create"]].drop_duplicates()
        df = df_unique.merge(df_roles, on="username")
        df = df.sort_values(by=["username"])
        return df.to_dict("records")

    def get_all_roles_list(self, engine):
        df = self.get_all_roles(engine)
        return df["role_name"].tolist()

    @expose("/")
    @admin_only
    @failure_tollerant
    def main(self):
        engine = self.get_edw_engine()
        database_name = self.get_edw_database()
        roles = self.get_roles_dependencies(engine)
        users = self.get_users(engine, database_name)
        return self.render_template("edw_grants.html", roles=roles, users=users)

    @expose("/delete_role", methods=["DELETE"])
    @admin_only
    @failure_tollerant_front_end
    def delete_role(self):
        engine = self.get_edw_engine()
        data = request.get_json()
        role_name = data.get("role_downstream")
        query = "drop role {role_name}"
        self.sanitize_identifiers([role_name])
        with engine.connect() as connection:
            connection.execute(text(query.format(role_name=role_name)))

    @expose("/delete_user", methods=["DELETE"])
    @admin_only
    @failure_tollerant_front_end
    def delete_user(self):
        engine = self.get_edw_engine()
        data = request.get_json()
        user_name = data.get("user_name")
        query = "drop user {user_name}"
        self.sanitize_identifiers([user_name])
        with engine.connect() as connection:
            connection.execute(text(query.format(user_name=user_name)))

    @expose("/add_role_page", methods=["GET", "POST"])
    @admin_only
    @failure_tollerant
    def add_role_page(self):
        engine = self.get_edw_engine()
        form = RolePermissionForm()
        form.roles.choices = self.get_all_roles_list(engine)
        create_role_q = "create role {role_name}"
        grant_role_q = "grant role {dependent_role} to role {role_name}"
        if form.validate_on_submit():
            role_name = form.role_name.data
            roles = form.roles.data
            self.sanitize_identifiers([role_name] + roles)
            with engine.connect() as connection:
                with connection.begin():
                    connection.execute(text(create_role_q.format(role_name=role_name)))
                    for dependent_role in roles:
                        connection.execute(
                            text(
                                grant_role_q.format(
                                    role_name=role_name, dependent_role=dependent_role
                                )
                            )
                        )
            flash(f"Role Name: {role_name}, Related Roles: {roles}", "success")
            return redirect(url_for("EdwGrantsAppBuilderBaseView.main"))
        return self.render_template("add_role.html", form=form)

    @expose("/edit_role_page/<string:role_name>/<string:roles>", methods=["GET", "PUT"])
    @admin_only
    @failure_tollerant
    def edit_role_page(self, role_name, roles):
        engine = self.get_edw_engine()
        form = RolePermissionForm()
        form.roles.choices = self.get_all_roles_list(engine)
        if request.method == "GET":
            form.roles.data = [role for role in roles.split(",")]
            form.role_name.data = role_name
            return self.render_template(
                "edit_role.html", form=form, role_name=role_name
            )
        if request.method == "PUT" and form.validate_on_submit():
            role_name = form.role_name.data
            roles = form.roles.data
            self.edit_roles_roles(engine, role_name, roles)
            flash(f"Role Name: {role_name}, Related Roles: {roles}", "success")
            return (
                jsonify(
                    {
                        "message": "Role updated successfully",
                        "role_name": role_name,
                        "roles": roles,
                    }
                ),
                200,
            )

    @expose("/edit_user_page/<string:user_name>/<string:roles>", methods=["GET", "PUT"])
    @admin_only
    @failure_tollerant
    def edit_user_page(self, user_name, roles):
        engine = self.get_edw_engine()
        form = AddRolesToUser()
        form.roles.choices = self.get_all_roles_list(engine)
        if request.method == "GET":
            form.roles.data = [role for role in roles.split(",")]
            form.user_name.data = user_name
            return self.render_template(
                "edit_user.html", form=form, user_name=user_name
            )
        if request.method == "PUT" and form.validate_on_submit():
            user_name = form.user_name.data
            roles = form.roles.data
            self.edit_users_roles(engine, user_name, roles)
            flash(f"User Name: {user_name}, Related Roles: {roles}", "success")
            return (
                jsonify({"message": "User updated successfully", "roles": roles}),
                200,
            )

    @expose("/add_user_page", methods=["GET", "POST"])
    @admin_only
    @failure_tollerant
    def add_user_page(self):
        engine = self.get_edw_engine()
        database_name = self.get_edw_database()
        form = NewUserForm()
        form.roles.choices = self.get_all_roles_list(engine)
        create_user_q = "create user {username} password :password"
        grant_role_q = "grant role {dependent_role} to {username}"
        grant_edit_database_q = "grant create on database {database_name} to {username}"
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            roles = form.roles.data
            can_edit_database = form.can_edit_database.data
            self.sanitize_identifiers([username, database_name] + roles)
            with engine.connect() as connection:
                with connection.begin():
                    connection.execute(
                        text(create_user_q.format(username=username)),
                        {"password": password},
                    )
                    for dependent_role in roles:
                        connection.execute(
                            text(
                                grant_role_q.format(
                                    username=username, dependent_role=dependent_role
                                )
                            )
                        )
                    if can_edit_database:
                        connection.execute(
                            text(
                                grant_edit_database_q.format(
                                    username=username, database_name=database_name
                                )
                            )
                        )
            flash(f"Username: {username}, Related Roles: {roles}", "success")
            return redirect(url_for("EdwGrantsAppBuilderBaseView.main"))
        return self.render_template("add_user.html", form=form)

    @expose("/update_edit_db_grant", methods=["PUT"])
    @admin_only
    @failure_tollerant_front_end
    def update_edit_db_grant(self):
        data = request.get_json()
        status = data.get("status")
        username = data.get("username")
        if status == "true":
            db_edit_grants_q = "grant create on database {database_name} to {username}"
        else:
            db_edit_grants_q = (
                "revoke create on database {database_name} from {username}"
            )
        engine = self.get_edw_engine()
        database_name = self.get_edw_database()
        with engine.connect() as connection:
            self.sanitize_identifiers([username, database_name])
            connection.execute(
                text(
                    db_edit_grants_q.format(
                        username=username, database_name=database_name
                    )
                )
            )


v_appbuilder_view = EdwGrantsAppBuilderBaseView()
v_appbuilder_package = {
    "name": "Permissions",
    "category": "EDW",
    "view": v_appbuilder_view,
}


class AirflowEdwGrantsPlugin(AirflowPlugin):
    name = "edw_grants_plugin"
    hooks = []
    macros = []
    flask_blueprints = [bp]
    appbuilder_views = [v_appbuilder_package]
    appbuilder_menu_items = []
