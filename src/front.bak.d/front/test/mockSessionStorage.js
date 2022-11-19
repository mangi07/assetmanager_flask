export const mockSessionStorage =  {
  _data: {},
  getItem: function (key) {
    return this._data[key]
  },
  setItem: function (key, val) {
    this._data[key] = val
  }
}

