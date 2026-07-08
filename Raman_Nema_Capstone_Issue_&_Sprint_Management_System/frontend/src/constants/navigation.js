export const ROUTES = {
  DASHBOARD: "/dashboard",
  PROJECTS: "/projects",
  SPRINTS: "/sprints",
  ISSUES: "/issues",
};

export const NAV_ITEMS = [
  {
    label: "Projects",
    path: ROUTES.PROJECTS,
  },
  {
    label: "Sprints",
    path: ROUTES.SPRINTS,
  },
  {
    label: "Issues",
    path: ROUTES.ISSUES,
  },
];

export const ADMIN_NAV_ITEMS = [
  {
    label: "Users",
    path: ROUTES.DASHBOARD,
  },
  ...NAV_ITEMS,
];
