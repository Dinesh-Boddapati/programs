const GREETING = ['Hello', 'Hi', 'Greetings', 'Welcome', 'Namaste', 'Hola', 'Bonjour', 'Ciao', 'Salam', 'Shalom'];

module.exports = async (req, res) => {
    res.send({
        greeting: GREETING[ Math.floor( Math.random() * GREETING.length )],
    });
};
