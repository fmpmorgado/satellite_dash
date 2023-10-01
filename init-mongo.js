db.createUser({
    user: 'teste',
    password: 'teste',
    roles: [
      {
        role: 'readWrite',
        db: 'test',
      },
    ],
  });