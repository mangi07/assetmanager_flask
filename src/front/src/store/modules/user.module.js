function resetUser (user, new_user=null) {
  if (new_user == null) {
    user.username = null
    user.role = null
    user.loggedIn = false
    user.error = null
    return;
  }
  user.username = new_user.username
  user.role = new_user.role
  user.loggedIn = new_user.loggedIn
  user.error = new_user.error
}

export const userModule = {
    namespaced: true,
    state: {
        user: {
            username: null,
            role: null,
            loggedIn: false,
            error: null,
        },
    },
    getters: {},
    mutations: {
        setUser (state, user) {
            resetUser(state.user, user)
        },
        unsetUser (state) {
            resetUser(state.user)
        },
    },
    actions: {
        setUserAction (context, user) {
            context.commit('setUser', user)
        },
        unsetUserAction (context) {
            context.commit('unsetUser')
        }
    },
}
