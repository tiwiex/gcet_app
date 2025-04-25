app_name = "gcet_apps"
app_title = "GCET Apps"
app_publisher = "Taiwo Akinosho"
app_description = "GCET Custom Apps"
app_email = "tiwiex@yahoo.com"
app_license = "mit"

# # Report overrides - Fixed format
override_doctype_class = {
    "Report": "gcet_apps.gcet_apps.report.modified_reports.report_controller.CustomReport"
}

# Include js files in header of desk.html
app_include_js = [
    "/assets/gcet_apps/js/financial_statements_with_fc.js"
]

# Report configurations
reports = [
    {
        "doctype": "Report",
        "name": "Financial Statements with FC",
        "report_name": "Financial Statements with FC",
        "module": "Accounts",
        "is_standard": "Yes",
        "ref_doctype": "GL Entry"
    }
]

# Force module refresh on session creation
on_session_creation = [
    "frappe.desk.moduleview.clear_cache"
]

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "gcet_apps",
# 		"logo": "/assets/gcet_apps/logo.png",
# 		"title": "GCET Apps",
# 		"route": "/gcet_apps",
# 		"has_permission": "gcet_apps.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/gcet_apps/css/gcet_apps.css"
# app_include_js = [
#     "js/financial_statements_with_fc.js"
#     #"/assets/gcet_apps/js/idelta_invoice_margin_analysis_report.js"
# ]

# Report initialization
report_config = [
    {
        "doctype": "Report",
        "name": "Financial Statements with FC",
        "report_name": "Financial Statements with FC",
        "module": "Accounts",
        "is_standard": "No",
        "ref_doctype": "GL Entry"
    }
]

# include js, css files in header of web template
# web_include_css = "/assets/gcet_apps/css/gcet_apps.css"
# web_include_js = "/assets/gcet_apps/js/gcet_apps.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "gcet_apps/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "gcet_apps/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "gcet_apps.utils.jinja_methods",
# 	"filters": "gcet_apps.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "gcet_apps.install.before_install"
# after_install = "gcet_apps.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "gcet_apps.uninstall.before_uninstall"
# after_uninstall = "gcet_apps.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "gcet_apps.utils.before_app_install"
# after_app_install = "gcet_apps.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "gcet_apps.utils.before_app_uninstall"
# after_app_uninstall = "gcet_apps.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "gcet_apps.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"gcet_apps.tasks.all"
# 	],
# 	"daily": [
# 		"gcet_apps.tasks.daily"
# 	],
# 	"hourly": [
# 		"gcet_apps.tasks.hourly"
# 	],
# 	"weekly": [
# 		"gcet_apps.tasks.weekly"
# 	],
# 	"monthly": [
# 		"gcet_apps.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "gcet_apps.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "gcet_apps.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "gcet_apps.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["gcet_apps.utils.before_request"]
# after_request = ["gcet_apps.utils.after_request"]

# Job Events
# ----------
# before_job = ["gcet_apps.utils.before_job"]
# after_job = ["gcet_apps.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"gcet_apps.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

