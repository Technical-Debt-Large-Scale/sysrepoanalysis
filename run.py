from msr import app
from msr import db, data_base
from msr.dao import User, Repository
import logging

CREATE_DB_EMPTY = False

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
    
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S', 
                filename='logs/my_app.log', filemode='w')

try:
    if CREATE_DB_EMPTY:
        db.drop_all()
        db.create_all()
        print(f'Data base {data_base} created with success!!')
    else:
        print(f'Data base {data_base} load successfully!')
    logging.info("Application started successfully!")
except Exception as e:
    print(f'Error creating {data_base} - {e}')
    logging.error("Exception occurred", exc_info=True)

if __name__ == '__main__':
    app.run(debug=True)
    