rs.initiate();

sleep(1000);

db = connect('mongodb://localhost:27017/admin');

db.createUser({
		"user": "root",
		"pwd": "root",
		"roles": [{"role": "root", "db": "admin"}]
});
