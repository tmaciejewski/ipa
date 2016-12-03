class CreateSchema:
    name = 'create_schema'
    desc = 'creates new DB schema'
    args = []

    def run(self, db, _):
        db.remove_schema()
        db.create_schema()
        db.commit()
