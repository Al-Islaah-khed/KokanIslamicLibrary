import { GoogleLogin } from '@react-oauth/google';
import { GoogleOAuthProvider } from '@react-oauth/google';

const LoginGoogle = () => {
    const handleSuccess = async ( credentialResponse ) => {
        const id_token = credentialResponse.credential;

        const res = await fetch( import.meta.env.VITE_BACKEND_BASE_URL + "/user/auth/login/google", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify( { id_token } ),
        } );

        const data = await res.json();
        // Save your app's JWT
        localStorage.setItem( "token", data.token );
    };

    return (
        <div>
            <h1>Login</h1>
            <GoogleOAuthProvider clientId="714278294233-bo5fov3d6decr0isfbf74tb3mjj2ifdf.apps.googleusercontent.com">
                <GoogleLogin onSuccess={ handleSuccess } onError={ () => alert( "Login Failed" ) } />
            </GoogleOAuthProvider>
            <br />
        </div>
    );
}

export default LoginGoogle
