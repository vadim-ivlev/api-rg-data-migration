import time
import save_rubrics

counter =0
while True:
    counter += 1
    print(f'main {counter}')
    save_rubrics.main()
    time.sleep(2)