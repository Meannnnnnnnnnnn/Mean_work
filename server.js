const express = require('express');
const path = require('path');
const app = express();
const port = 3000;

app.use(express.static(path.join(__dirname, 'map_web_interface')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'map_web_interface', 'index.html'));
});

app.listen(port, () => {
    console.log(`Web app listening at http://localhost:${port}`);
});
