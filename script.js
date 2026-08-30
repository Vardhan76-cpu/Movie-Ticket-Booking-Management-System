let shows=[];
const $=id=>document.getElementById(id);
async function load(){shows=await (await fetch("/api/shows")).json();$("show").innerHTML='<option value="">Select a show</option>';
shows.forEach(s=>{let o=document.createElement("option");o.value=s.id;o.textContent=`${s.movie_name} — ${s.theatre_name} — ${s.show_date} ${s.show_time} — ₹${s.ticket_price} (${s.available_seats} seats)`;$("show").appendChild(o)})}
function update(){let s=shows.find(x=>String(x.id)==$("show").value),n=+$("tickets").value||0;$("info").innerHTML=s?`<b>${s.movie_name}</b><br>${s.theatre_name}, ${s.location}<br>${s.show_date} at ${s.show_time}<br>Type: ${s.show_type} • Available: ${s.available_seats}`:"";$("cost").textContent=`Total Cost: ₹${s?s.ticket_price*n:0}`}
$("show").onchange=update;$("tickets").oninput=update;
$("form").onsubmit=async e=>{e.preventDefault();let p={customer_name:$("name").value,email:$("email").value,phone:$("phone").value,show_id:+$("show").value,tickets:+$("tickets").value};
let r=await fetch("/api/bookings",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(p)}),d=await r.json();
$("result").innerHTML=r.ok?`<h2>✅ Booking Confirmed</h2><p><b>Booking ID:</b> ${d.booking_id}</p><p>${d.movie} — ${d.theatre}</p><p>${d.show_date} ${d.show_time} • ${d.tickets} ticket(s) • ₹${d.total_cost}</p><img width="150" src="${d.qr_url}">`:`<h2>❌ ${d.error}</h2>`;await load();update()};
async function findBooking(){let id=$("bid").value.trim(),r=await fetch("/api/bookings/"+encodeURIComponent(id)),d=await r.json();$("lookup").innerHTML=r.ok?`<p><b>${d.booking_id}</b> — ${d.status}<br>${d.movie_name} at ${d.theatre_name}<br>${d.show_date} ${d.show_time} • ${d.tickets} ticket(s) • ₹${d.total_cost}</p>`:`<p>${d.error}</p>`}
async function cancelBooking(){let id=$("bid").value.trim();if(!id)return alert("Enter booking ID");if(!confirm("Cancel this booking?"))return;let r=await fetch("/api/bookings/"+encodeURIComponent(id)+"/cancel",{method:"POST"}),d=await r.json();$("lookup").innerHTML=`<p>${d.message||d.error}</p>`;await load();update()}
load();