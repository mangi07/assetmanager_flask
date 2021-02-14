function addAssets (state, assets) {
    Object.keys(assets).forEach(function(key) {
        var asset = assets[key]
        state.assets.push(
            asset
        )
    })
}

export const assetsModule = {
    namespaced: true,
    state: {
        assets: [],
    },
    getters: {},
    mutations: {
        appendAssets (state, assets) {
            addAssets(state, assets)
        },
        getNewAssets (state, assets) {
            state.assets = []
            addAssets(state, assets)
        },
    },
    actions: {
        appendAssetsAction (context, response) {
            context.commit('appendAssets', response.data.assets)
        },
        getNewAssetsAction (context, response) {
            context.commit('getNewAssets', response.data.assets)
        }
    },
}