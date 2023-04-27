-- app_role
DROP TABLE IF EXISTS public.app_role;
CREATE SEQUENCE IF NOT EXISTS app_role_id_seq;
CREATE TABLE public.app_role (
	role_id int4 NOT NULL DEFAULT nextval('app_role_id_seq'::regclass),
	role_name text NOT NULL DEFAULT 'Neuer Benutzertyp'::text,
	"locked" bool NOT NULL DEFAULT true,
	CONSTRAINT app_role_pkey PRIMARY KEY (role_id)
);

INSERT INTO "public"."app_role" ("role_id", "role_name", "locked") VALUES
(1, 'Administrator', 't'),
(2, 'User', 't');

-- app_permission_group
DROP TABLE IF EXISTS public.app_permission_group;
CREATE SEQUENCE IF NOT EXISTS app_permission_group_id_seq;
CREATE TABLE public.app_permission_group (
	permission_group_id int4 NOT NULL DEFAULT nextval('app_permission_group_id_seq'::regclass),
	permission_group_name text NOT NULL DEFAULT 'permission_group_x'::text,
	CONSTRAINT app_permission_group_permission_group_name_key UNIQUE (permission_group_name),
	CONSTRAINT app_permission_group_pkey PRIMARY KEY (permission_group_id)
);

INSERT INTO "public"."app_permission_group" ("permission_group_id", "permission_group_name") VALUES
(1, 'internal');

-- app permission
DROP TABLE IF EXISTS public.app_permission;
CREATE SEQUENCE IF NOT EXISTS app_permission_id_seq;
CREATE TABLE public.app_permission (
	permission_id int4 NOT NULL DEFAULT nextval('app_permission_id_seq'::regclass),
	permission_key text NOT NULL DEFAULT 'can_do_x'::text,
	permission_group_id int4 NULL,
	CONSTRAINT app_permission_permission_key_key UNIQUE (permission_key),
	CONSTRAINT app_permission_pkey PRIMARY KEY (permission_id),
	CONSTRAINT app_permission_permission_group_id_fkey FOREIGN KEY (permission_group_id) REFERENCES public.app_permission_group(permission_group_id)
);

INSERT INTO "public"."app_permission" ("permission_id", "permission_key", "permission_group_id") VALUES
(1, 'users_can_view_user_list', 1),
(2, 'users_can_create_user', 1),
(3, 'users_can_edit_other_users', 1),
(4, 'roles_can_view_role_list', 1),
(5, 'roles_can_create_edit_role', 1),
(6, 'permissions_can_view_permission_list', 1),
(7, 'pages_can_view_overview', 1),
(8, 'pages_can_view_articles_internal', 1),
(9, 'pages_can_view_articles_supplier', 1),
(10, 'pages_can_view_analysis', 1),
(11, 'pages_can_view_settings', 1);

-- app_user
DROP TABLE IF EXISTS public.app_user;
CREATE SEQUENCE IF NOT EXISTS app_user_id_seq;
CREATE TABLE public.app_user (
	user_id int4 NOT NULL DEFAULT nextval('app_user_id_seq'::regclass),
	email varchar NOT NULL,
	first_name varchar NOT NULL,
	last_name varchar NOT NULL,
	enabled bool NOT NULL DEFAULT true,
	"language" varchar NULL DEFAULT 'DE'::character varying,
	pw_hash varchar NOT NULL,
	pw_reset_required bool NOT NULL DEFAULT true,
	role_id int4 NULL,
	CONSTRAINT app_user_email_key UNIQUE (email),
	CONSTRAINT app_user_pkey PRIMARY KEY (user_id),
	CONSTRAINT app_user_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.app_role(role_id)
);
INSERT INTO "public"."app_user" ("user_id", "email", "first_name", "last_name", "enabled", "language", "pw_hash", "pw_reset_required", "role_id") VALUES
(1, 'administrator@test.com', 'Admin', 'Admin', 't', 'DE', 'pbkdf2:sha256:260000$prfouHlp1hM3vpbW$c5e859e6d5bf8dc9890c0d291b380e748abe1d324a574113e139395d1c23490e', 'f', 1),
(2, 'username@test.com', 'User', 'User', 't', 'DE', 'pbkdf2:sha256:260000$GCru1WNe7MoJ7Id4$58d15eaec20f57f5b2f6814c8566a6dac21f911898553b17e568e4ae5473862d', 't', 2);

-- app_roles_permissions
DROP TABLE IF EXISTS public.app_roles_permissions;
CREATE TABLE public.app_roles_permissions (
	role_id int4 NOT NULL,
	permission_id int4 NOT NULL,
	CONSTRAINT app_roles_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.app_permission(permission_id) ON DELETE CASCADE,
	CONSTRAINT app_roles_permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.app_role(role_id) ON DELETE CASCADE
);

INSERT INTO "public"."app_roles_permissions" ("role_id", "permission_id") VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(1, 6),
(1, 7),
(1, 8),
(1, 9),
(1, 10),
(1, 11),
(2, 7),
(2, 8),
(2, 9),
(2, 10),
(2, 11);

-- make sure sequences are in consistent state
SELECT setval('public.app_permission_id_seq', (SELECT MAX(permission_id) AS max_id FROM app_permission));
SELECT setval('public.app_permission_group_id_seq', (SELECT MAX(permission_group_id) AS max_id FROM app_permission_group));
SELECT setval('public.app_role_id_seq', (SELECT MAX(role_id) AS max_id FROM app_role));
SELECT setval('public.app_user_id_seq', (SELECT MAX(user_id) AS max_id FROM app_user));

-- celery_tasks
DROP TABLE IF EXISTS public.celery_tasks;
CREATE SEQUENCE IF NOT EXISTS celery_tasks_id_seq;
CREATE TABLE public.celery_tasks (
    id int4 NOT NULL DEFAULT nextval('celery_tasks_id_seq'::regclass),
	task_id varchar NOT NULL,
	user_id  int4 NOT NULL,
    creation_date timestamp NOT NULL DEFAULT NOW(),
    task_status varchar NOT NULL,
    last_modified timestamp NOT NULL DEFAULT NOW(),
	CONSTRAINT celery_tasks_pkey PRIMARY KEY (id)
);