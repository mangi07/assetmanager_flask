export const locationsModule = {
    namespaced: true,
    state: {
        locations: {},
    },
    getters: {},
    mutations: {
        getNewLocations (state, locations) {
            state.locations = {}
            state.locations = locations
        },
    },
    actions: {
        appendLocationsAction (context, locs) {
            context.commit('appendLocations', locs)
        },
        getNewLocationsAction (context, locs) {
            context.commit('getNewLocations', locs)
        }
    },
}
