/* Address lookup boundary: replace this provider when using an external map API.
   Nothing here imports pricing, SQL, or the cost engine. No network requests. */
function createFixtureDistanceProvider(addresses) {
 const records = JSON.parse(JSON.stringify(addresses));
 return {
  listAddresses() { return records.map(a=>({...a,distances_miles:{...a.distances_miles}})); },
  async resolve(addressId) {
   const row = records.find(a=>a.address_id===addressId);
   if(!row) throw new Error('Unknown predefined address: '+addressId);
   return {...row,distances_miles:{...row.distances_miles},source:'Predetermined test distances (not a map lookup)'};
  }
 };
}
if(typeof module!=='undefined') module.exports={createFixtureDistanceProvider};
