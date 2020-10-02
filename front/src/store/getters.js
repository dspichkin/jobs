const getters = {
  sidebar: state => state.app.sidebar,
  language: state => state.app.language,
  size: state => state.app.size,
  device: state => state.app.device,
  roles: state => state.user.roles,
  status: state => state.user.status,
  setting: state => state.user.setting,
  token: state => state.user.token,
  avatar: state => state.user.avatar,
  name: state => state.user.name,
  // categories: state => state.search_domains.search_domains,
  /*
  visitedViews: state => state.tagsView.visitedViews,
  cachedViews: state => state.tagsView.cachedViews,
  introduction: state => state.user.introduction,
  errorLogs: state => state.errorLog.logs,
  permission_routers: state => state.permission.routers,
  addRouters: state => state.permission.addRouters,
  */
  permission_routers: state => state.permission.routers
}
export default getters
