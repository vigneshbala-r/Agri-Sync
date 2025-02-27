body {
    margin: 0;
    padding: 0;
    font-family: 'Arial', sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: linear-gradient(135deg, #4CAF50, #C8E6C9);
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;

    overflow: hidden;
    animation: grayscaleAnimation 5s infinite;
}



/* Login Container */
.login-container {
    text-align: center;
    
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0 4px 15px 
    rgba(219, 7, 231, 0.2);
    max-width: 400px;
    width: 100%;
    background: rgba(255, 255, 255, 0.9); 
}

.login-container h1 {
    font-size: 2.5rem;
    color: #40aa43;
    margin-bottom: 10px;
}

.login-container p {
    font-size: 1.1rem;
    color: #555;
    margin-bottom: 30px;
}

/* Form Styles */
.form-group {
    margin-bottom: 20px;
    text-align: left;
}

.form-group label {
    font-size: 1rem;
    color: #333;
    font-weight: bold;
    display: block;
    margin-bottom: 5px;
}

.input-icon {
    position: relative;
}

.input-icon input {
    width: 350px;
    padding: 10px 40px 10px 15px;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 8px;
    outline: none;
    transition: border-color 0.3s ease;
}

.input-icon input:focus {
    border-color: #4CAF50;
}

.input-icon img {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    width: 22px;
    height: 20px;
    cursor: pointer;
}

/* Login Button */
.login-btn {
    width: 100%;
    padding: 12px;
    font-size: 1rem;
    font-weight: bold;
    color: #fff;
    background-color: #4CAF50;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.login-btn:hover {
    background-color: #45a049;
}

/* Sign Up Link */
.signup-link {
    margin-top: 15px;
    font-size: 0.9rem;
    color: #555;
}

.signup-link a {
    color: #4CAF50;
    text-decoration: none;
    font-weight: bold;
}

.signup-link a:hover {
    text-decoration: underline;
}