import {login, logout, getInfo, getPubKey} from '@/api/user'
import {getToken, setToken, removeToken} from '@/utils/auth'
import {resetRouter} from '@/router'
import {JSEncrypt} from 'jsencrypt'

const getDefaultState = () => {
  return {
    token: getToken(),
    name: '',
    avatar: ''
  }
}

const state = getDefaultState()

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  }
}

const actions = {
  // user login

  async login({commit}, userInfo) {
    const {username, password} = userInfo
    let {data} = await getPubKey()
    const encryptor = new JSEncrypt() // 新建JSEncrypt对象
    encryptor.setPublicKey(data)
    const passwordEncryp = encryptor.encrypt(password)

    console.log(passwordEncryp)

    // return login({username: username.trim(), password: password})

    return new Promise((resolve, reject) => {
      login({username: username.trim(), password: passwordEncryp}).then(response => {
        const {data} = response
        commit('SET_TOKEN', data.access)
        setToken(data.access)
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // get user info
  getInfo({commit, state}) {
    return new Promise((resolve, reject) => {
      getInfo(state.token).then(response => {
        const {data} = response

        if (!data) {
          return reject('Verification failed, please Login again.')
        }

        const {username, avatar} = data

        commit('SET_NAME', username)
        commit('SET_AVATAR', avatar)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // user logout
  logout({commit, state}) {
    return new Promise((resolve, reject) => {
      logout(state.token).then(() => {
        removeToken() // must remove  token  first
        resetRouter()
        commit('RESET_STATE')
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // remove token
  resetToken({commit}) {
    return new Promise(resolve => {
      removeToken() // must remove  token  first
      commit('RESET_STATE')
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

