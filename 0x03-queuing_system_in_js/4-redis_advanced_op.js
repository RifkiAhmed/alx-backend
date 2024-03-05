import redis from 'redis';

const client = redis.createClient()
  .on('error', err => console.log(`Redis client not connected to the server: ${err.message}`))
  .on('connect', () => console.log('Redis client connected to the server'));

function createHash() {
  client.hset('HolbertonSchools', 'Portland', 50, redis.print);
  client.hset('HolbertonSchools', 'Seattle', 80, redis.print);
  client.hset('HolbertonSchools', 'New York', 20, redis.print);
  client.hset('HolbertonSchools', 'Bogota', 20, redis.print);
  client.hset('HolbertonSchools', 'Cali', 40, redis.print);
  client.hset('HolbertonSchools', 'Paris', 2, redis.print);
}

function displayHash() {
  client.hgetall('HolbertonSchools', (err, reply) => {
    console.log(reply);
  });
}
  
createHash();
displayHash();
