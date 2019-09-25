export const assetsModule = {
    namespaced: true,
    state: {
        assets: [],
    },
    getters: {},
    mutations: {
        appendAssets (state, assets) {
            Object.keys(assets).forEach(function(key) {
                console.log(key, assets[key]);
                var asset = assets[key]
                state.assets.push(
                    asset
                )
            })
        },
    },
    actions: {
        appendAssetsAction (context, assets) {
            console.log(assets)
            context.commit('appendAssets', assets)
        },
    },
}