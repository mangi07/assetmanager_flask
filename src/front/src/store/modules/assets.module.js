function assertResponseStructureIsValid (response) {
    return ! (response.data == undefined
        || response.data.assets == undefined
	|| (response.data.prev == undefined && response.data.next == undefined)
    );
}

function addAssets (state, response) {
    Object.keys(response.data.assets).forEach(function(key) {
        var asset = response.data.assets[key]
        state.assets.push(
            asset
        )
    })

    // TODO: check that this is the correct json structure sent from the server
    console.log("DEBUG: What is the structure of the object passed in to this addAssets function?");
    console.log(response);
    console.log(assertResponseStructureIsValid(response));

    state.pagination.prev = response.data.prev;
    //console.info(`state.pagination.prev ${state.pagination.prev}`);
    state.pagination.next = response.data.next;
    //console.info(`state.pagination.next ${state.pagination.next}`);
}

export const assetsModule = {
    namespaced: true,
    state: {
        assets: [],
	pagination: {
		prev: null,
		next: null,
	},
    },
    getters: {},
    mutations: {
        appendAssets (state, data) {
            addAssets(state, data)
        },
        getNewAssets (state, data) {
            state.assets = []
            addAssets(state, data)
        },
    },
    actions: {
        appendAssetsAction (context, response) {
            context.commit('appendAssets', response)
        },
        getNewAssetsAction (context, response) {
            context.commit('getNewAssets', response)
        },
    },
}
