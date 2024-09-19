"use client"

import { useState } from 'react';


export default function RegisterComponent() {

    function ButtonClick(){
        console.log("Esto no va")
    }

    const [count, setCount] = useState(0)

    return (
        <div className="flex justify-center align-center h-full w-full p-[25px] gap-4 flex-col">
            <h1>Register form: <b>{count}</b></h1>
            <form>
                <input type="email" name="email" placeholder="Email" required />
                <input type="password" name="password" placeholder="Password" required />
                <button type="submit" onClick={() => setCount(count+1)}>Login</button>
            </form>
        </div>
    );
}


