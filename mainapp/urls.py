from django.urls import include, path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("health", views.health.health, name="health"),
    path(
        "privacy/",
        TemplateView.as_view(template_name="mainapp/privacy.html"),
        name="privacy",
    ),
    path(
        "callbacks/authorize",
        views.AuthorizeCallbackView.as_view(),
        name="authorize-callback",
    ),
    path("me/", views.user.UserUpdateView.as_view(), name="profile"),
    path("me/delete", views.user.UserDeleteView.as_view(), name="profile_delete"),
    # Metrics
    path(
        "metrics/",
        include(
            [
                path("", views.metric.MetricListView.as_view(), name="metrics"),
                path(
                    "<uuid:pk>/",
                    include(
                        [
                            path(
                                "",
                                views.metric.MetricUpdateView.as_view(),
                                name="metric-details",
                            ),
                            # Markers
                            path(
                                "markers/",
                                include(
                                    [
                                        path("", views.marker.marker, name="marker"),
                                        path(
                                            "<str:marker_date_str>",
                                            views.marker.marker_with_date,
                                            name="marker",
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
                path(
                    "<uuid:pk>/backfill",
                    views.metric.metric_backfill,
                    name="metric-backfill",
                ),
                path(
                    "<uuid:pk>/delete",
                    views.metric.MetricDeleteView.as_view(),
                    name="metric_delete",
                ),
                path(
                    "<uuid:pk>/transfer_ownership",
                    views.metric.MetricTransferOwnershipView.as_view(),
                    name="metric_transfer_ownership",
                ),
                path(
                    "<uuid:pk>/authorize",
                    views.metric.metric_authorize,
                    name="metric-authorize",
                ),
                path(
                    "<uuid:pk>/select-integration",
                    views.metric.MetricIntegrationUpdateView.as_view(),
                    name="metric-select-integration",
                ),
                path(
                    "<uuid:pk>/test",
                    views.metric.metric_test,
                    name="metric-test",
                ),
                path(
                    "<uuid:pk>/duplicate",
                    views.metric.metric_duplicate,
                    name="metric-duplicate",
                ),
                path(
                    "<uuid:pk>/import",
                    views.metric.MetricImportView.as_view(),
                    name="metric-import",
                ),
                path(
                    "<uuid:pk>/dashboards/add",
                    views.metric.MetricDashboardAddView.as_view(),
                    name="metricdashboard_add",
                ),
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
                    "new/<state>/select-integration",
                    views.metric.NewMetricIntegrationCreateView.as_view(),
                    name="metric-new-with-state-select-integration",
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
                                "orgusers/<int:organization_user_pk>",
                                views.organization.OrganizationUserUpdateView.as_view(),
                                name="organization_user_edit",
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
                            path(
                                "authorize_slack_notifications",
                                views.organization.authorize_slack_notifications,
                                name="organization_authorize_slack_notifications",
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
        view=views.organization_invitation.InvitationListView.as_view(),
        name="invitation_list",
    ),
    path(
        "invitations/<key>",
        view=views.organization_invitation.InvitationAcceptView.as_view(),
        name="invitation_accept",
    ),
    # Dashboards
    path(
        "dashboards/",
        include(
            [
                path(
                    "",
                    view=views.dashboard.index,
                    name="dashboards",
                ),
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
                    "<int:dashboard_pk>/metrics/<uuid:metric_pk>/remove",
                    view=views.dashboard.DashboardMetricRemoveView.as_view(),
                    name="dashboardmetric_remove",
                ),
                path(
                    "<int:pk>/transfer_ownership",
                    views.dashboard.DashboardTransferOwnershipView.as_view(),
                    name="dashboard_transfer_ownership",
                ),
            ]
        ),
    ),
    # Dashboards
    path(
        "<username_or_org_slug>/<dashboard_slug>",  # this one needs to be at the bottom
        views.dashboard.dashboard_view,
        name="dashboard",
    ),
]
