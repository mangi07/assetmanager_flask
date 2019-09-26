export const assetsModule = {
    namespaced: true,
    state: {
        assets: [],
    },
    getters: {},
    mutations: {
        appendAssets (state, assets) {
            Object.keys(assets).forEach(function(key) {
                var asset = assets[key]
                state.assets.push(
                    asset
                )
            })
        },
    },
    actions: {
        appendAssetsAction (context, response) {
            context.commit('appendAssets', response.data.assets)
        },
    },
}