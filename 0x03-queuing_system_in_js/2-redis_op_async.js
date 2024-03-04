import redis from 'redis';
import { promisify } from 'util';

const client = redis.createClient()
  .on('error', err => console.log(`Redis client not connected to the server: ${err.message}`))
  .on('connect', () => console.log('Redis client connected to the server'));

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print('Reply: OK'));
}

const getAsync = promisify(client.get).bind(client);

async function displaySchoolValue(schoolName) {
  const reply = await getAsync(schoolName);
  console.log(reply);
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
