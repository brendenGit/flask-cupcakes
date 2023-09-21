const cupcakeList = document.getElementById('cupcakesList');

document.getElementById('addCupcakeForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        flavor: document.getElementById('flavor').value,
        size: document.getElementById('size').value,
        rating: document.getElementById('rating').value,
        image: document.getElementById('image').value
    };

    await axios.post('/api/cupcakes', formData)
    while (cupcakeList.firstChild) {
        cupcakeList.removeChild(cupcakeList.firstChild);
    }
    showCupcakes();
});

async function showCupcakes() {
    const response = await axios.get("/api/cupcakes");
    const cupcakes = response.data.cupcakes;
    for (const cupcake of cupcakes) {
        c = document.createElement('li');
        c.innerText = `${cupcake.flavor} | ${cupcake.rating} | ${cupcake.size}`;
        cupcakeList.append(c);
    }
    return cupcakes;
}

showCupcakes()