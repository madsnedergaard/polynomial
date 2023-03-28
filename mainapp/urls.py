from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "callbacks/authorize",
        views.AuthorizeCallbackView.as_view(),
        name="authorize-callback",
    ),
    # Metrics
    path(
        "metrics/",
        include(
            [
                path("", views.metric.MetricListView.as_view(), name="metrics"),
                path(
                    "<int:pk>/",
                    views.metric.MetricUpdateView.as_view(),
                    name="metric-details",
                ),
                path(
                    "<int:pk>/backfill",
                    views.metric.metric_backfill,
                    name="metric-backfill",
                ),
                path(
                    "<int:pk>/collect_latest",
                    views.metric.metric_collect_latest,
                    name="metric-collect-latest",
                ),
                path(
                    "<int:pk>/delete",
                    views.metric.MetricDeleteView.as_view(),
                    name="metric_delete",
                ),
                path(
                    "<int:pk>/authorize",
                    views.metric.metric_authorize,
                    name="metric-authorize",
                ),
                path(
                    "<int:pk>/test",
                    views.metric.metric_test,
                    name="metric-test",
                ),
                path(
                    "<int:pk>/duplicate",
                    views.metric.metric_duplicate,
                    name="metric-duplicate",
                ),
                # path(
                #     "<int:pk>/import",
                #     views.metric.metric_import,
                #     name="metric-import",
                # ),
                # These are metric creation routes, which use the cache as backend
                path(
                    "new",
                    views.metric.metric_new,
                    name="metric_new",
                ),
                path(
                    "new/<state>/",
                    views.metric.MetricCreateView.as_view(),
                    name="metric-new-with-state",
                ),
                path(
                    "new/<state>/authorize",
                    views.metric.metric_new_authorize,
                    name="metric-new-with-state-authorize",
                ),
                path(
                    "new/<state>/test",
                    views.metric.metric_new_test,
                    name="metric-new-with-state-test",
                ),
            ]
        ),
    ),
    # Integrations (i.e. metric, and thus, db independent)
    path(
        "integrations/",
        views.IntegrationListView.as_view(),
        name="integrations",
    ),
    # Orgs
    path(
        "orgs/",
        include(
            [
                path(
                    "",
                    views.organization.OrganizationListView.as_view(),
                    name="organization_list",
                ),
                path(
                    "new",
                    views.organization.OrganizationCreateView.as_view(),
                    name="organization_new",
                ),
                path(
                    "<int:organization_pk>/",
                    include(
                        [
                            path(
                                "edit",
                                views.organization.OrganizationUpdateView.as_view(),
                                name="organization_edit",
                            ),
                            path(
                                "delete",
                                views.organization.OrganizationDeleteView.as_view(),
                                name="organization_delete",
                            ),
                            path(
                                "orgusers/",
                                views.organization.OrganizationUserListView.as_view(),
                                name="organization_user_list",
                            ),
                            path(
                                "orgusers/new",
                                views.organization.OrganizationUserCreateView.as_view(),
                                name="organization_user_new",
                            ),
                            path(
                                "orgusers/<int:organization_user_pk>/delete",
                                views.organization.OrganizationUserDeleteView.as_view(),
                                name="organization_user_delete",
                            ),
                            path(
                                "authorize_google_spreadsheet_export",
                                views.organization.authorize_google_spreadsheet_export,
                                name="organization_authorize_google_spreadsheet_export",
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
    # Invitations
    path(
        "invitations/",
        view=views.InvitationListView.as_view(),
        name="invitation_list",
    ),
    path(
        "invitations/<key>",
        view=views.InvitationAcceptView.as_view(),
        name="invitation_accept",
    ),
    # Dashboards
    path(
        "dashboards/",
        include(
            [
                path(
                    "new",
                    view=views.dashboard.DashboardCreateView.as_view(),
                    name="dashboard_new",
                ),
                path(
                    "<int:dashboard_pk>/delete",
                    view=views.dashboard.DashboardDeleteView.as_view(),
                    name="dashboard_delete",
                ),
                path(
                    "<int:dashboard_pk>/edit",
                    view=views.dashboard.DashboardUpdateView.as_view(),
                    name="dashboard_edit",
                ),
                path(
                    "<int:dashboard_pk>/metrics/add",
                    view=views.dashboard.DashboardMetricAddView.as_view(),
                    name="dashboardmetric_add",
                ),
                path(
                    "<int:dashboard_pk>/metrics/<int:metric_pk>/remove",
                    view=views.dashboard.DashboardMetricRemoveView.as_view(),
                    name="dashboardmetric_remove",
                ),
            ]
        ),
    ),
    # User pages
    path(
        "<username_or_org_slug>/",  # this one needs to be at the bottom
        views.page,
        name="page",
    ),
    # Dashboards
    path(
        "<username_or_org_slug>/<dashboard_slug>",  # this one needs to be at the bottom
        views.dashboard.dashboard_view,
        name="dashboard",
    ),
]
