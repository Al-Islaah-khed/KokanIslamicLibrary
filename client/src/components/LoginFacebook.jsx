import React from "react";
import FacebookLogin from "react-facebook-login";
import axios from "axios";


const LoginFacebook = () => {
    const handleFacebookLogin = async ( response ) => {
        if ( response.accessToken ) {
            try {
                const res = await axios.post( import.meta.env.VITE_BACKEND_BASE_URL + "/user/auth/login/facebook", {
                    access_token: response.accessToken,
                } );

                console.log( "Login Success:", res.data );
                localstorage.setItem( res.data.token )
                // Save token to localStorage/cookies, update UI, etc.
            } catch ( error ) {
                console.error( "Login Failed:", error.response?.data || error.message );
            }
        }
    };

    return (
        <FacebookLogin
            appId="4114755208769700"
            autoLoad={ false }
            fields="name,email,picture"
            callback={ handleFacebookLogin }
            icon="fa-facebook"
        />
    );
};

export default LoginFacebook;
