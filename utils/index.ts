import axios from 'axios'

export const API = process.env.SERVER_API;

export const fetcher = (url: string) => axios.get(url).then(r => r.data.message).catch(err => err)
