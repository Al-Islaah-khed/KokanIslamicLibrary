import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import LoginGoogle from './components/LoginGoogle'
import LoginFacebook from './components/LoginFacebook'


function App () {
  return ( <>
    <LoginGoogle />
    <LoginFacebook />
  </> )
}

export default App
