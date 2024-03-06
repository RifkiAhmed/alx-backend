const express = require('express');
const redis = require('redis');

import { promisify } from 'util';

const app = express();
app.listen(1245);

const listProducts = [
  {
    Id: 1, name: 'Suitcase 250', price: 50, stock: 4
  },
  {
    Id: 2, name: 'Suitcase 450', price: 100, stock: 10
  },
  {
    Id: 3, name: 'Suitcase 650', price: 350, stock: 2
  },
  {
    Id: 4, name: 'Suitcase 1050', price: 550, stock: 5
  }
];

const client = redis.createClient()
  .on('error', err => console.log(`Redis client not connected to the server: ${err.message}`));

const getAsync = promisify(client.get).bind(client);

function getItemById(id) {
  const item = listProducts.find(item => item.Id === id);
  return item;
}

function reserveStockById(itemId, stock) {
  client.set(`item.${itemId}`, stock);
}

async function getCurrentReservedStockById(itemId) {
  const stock = await getAsync(`item.${itemId}`);
  return stock ? parseInt(stock): 0;
}

app.get('/list_products', (req, res) => {
  res.send(JSON.stringify(listProducts.map(product => {
    return {
      itemId: product.Id,
      itemName: product.name,
      price: product.price,
      initialAvailableQuantity: product.stock
    }})
  ));
});

app.get('/list_products/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const item = getItemById(parseInt(itemId));
  if (!item) {
    res.send({"status": "Product not found"});
  }
  const currentReservedStock = await getCurrentReservedStockById(itemId);
  const availableStock = parseInt(item.stock) - currentReservedStock
  const currentProduct = {
	  itemId: item.Id,
	  itemName: item.name,
	  price: item.price,
	  currentQuantity: availableStock};
  res.send(JSON.stringify(currentProduct));
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const item = getItemById(parseInt(itemId));
  if (!item) {
    res.send({"status": "Product not found"});
  }
  const currentReservedStock = await getCurrentReservedStockById(itemId);
  const availableStock = item.initialAvailableQuantity - currentReservedStock;
  if (availableStock <= 0) {
    res.send({"status":"Not enough stock available", "itemId": item.Id});
  }
  reserveStockById(itemId, currentReservedStock + 1);
  res.send({"status":"Reservation confirmed", "itemId": item.Id});
});

module.exports = app;
