import '@/styles/globals.css'
// import { NextPage } from "next";
import type { AppProps } from 'next/app'

const App = ({ Component, pageProps }: AppProps) => {
  // const Page: NextPage = Component;
  return <Component {...pageProps} />
}
export default App;
