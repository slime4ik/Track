import {Header} from "../Header/Header.jsx";
import "./RegistrationPage.css"
import {Form} from "react-router-dom";
import {useState} from "react";
import useFetch from "../../Hooks/useFetch.jsx";

export default function RegistrationPage() {
    const [email, setEmail] = useState("")
    const [username, setUsername] = useState("")

    function handleSuccessfulRegistration(data) {
        console.log(data)
    }

    function register(e) {
        e.preventDefault()

        useFetch("http://localhost:8000/api/registration/", handleSuccessfulRegistration, {
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