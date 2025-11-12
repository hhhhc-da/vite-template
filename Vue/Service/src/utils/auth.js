import Cookies from 'js-cookie'

const TOKEN_KEY = 'user_token'
const USERNAME_KEY = 'user_name'

export const setLoginCookie = (username, token) => {
  Cookies.set(USERNAME_KEY, username, { expires: 1/24 })
  Cookies.set(TOKEN_KEY, token, { expires: 1/24 })
}

export const getUsername = () => {
  return Cookies.get(USERNAME_KEY) || ''
}

export const getToken = () => {
  return Cookies.get(TOKEN_KEY) || ''
}

export const removeLoginCookie = () => {
  Cookies.remove(USERNAME_KEY)
  Cookies.remove(TOKEN_KEY)
}

export const isLogin = () => {
  return !!getToken()
}