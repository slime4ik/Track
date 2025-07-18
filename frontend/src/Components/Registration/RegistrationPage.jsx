import {Header} from "../Header/Header.jsx";
import "./RegistrationPage.css"
import {Form, useNavigate} from "react-router-dom";
import {useState} from "react";
import useFetch from "../../Hooks/useFetch.jsx";
import Cookies from 'universal-cookie';

export default function RegistrationPage() {
    const [email, setEmail] = useState("")
    const [username, setUsername] = useState("")
    const [error, setError] = useState(null)
    const navigate = useNavigate();

    function handleSuccessfulRegistration(json) {
        const cookies = new Cookies(null, { path: '/' });

        cookies.set('registration_token', json['reg_token']);

        if (cookies.get('registration_token') == null) {
            setError({message: "Не удалось установить куки"})
        }

        navigate("enter_code")
    }

    function handleError(jsonError) {
        setError(jsonError)
    }

    function register(e) {
        e.preventDefault()

        useFetch("http://localhost:8000/api/registration/", handleSuccessfulRegistration, handleError, {
            method: "post",
            body: JSON.stringify({username, email}),
            headers: {
                "Content-Type": "application/json"
            }
        })
    }

    return (
        <>
            <Header />
            <div id="registration_container">
                {error && <div id="registration_error_block">
                    {JSON.stringify(error, null, 2)}
                </div>}
                <div id="registration_block">
                    <Form id="registration_form" onSubmit={register}>
                        <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="Емаил" name="email"/>
                        <input type="text" value={username} onChange={e => setUsername(e.target.value)} placeholder="Юзернаме" name="username" maxLength="30" minLength="2"/>
                        <button type="submit">Зарегистрироваться</button>
                    </Form>
                </div>
            </div>
        </>
    )
}