from collections.abc import Iterable
import sys, builtins, time

class looprint:
  def __init__(self, data : Iterable, loopName : str = "Loop") -> None:
    if not isinstance(data, Iterable): raise TypeError(f"LooPrint argument must be Iterable, {type(data).__name__} provided")
    self.data = data
    self.name = loopName
    self.msg = None
    
  def __iter__(self):
    def newPrint(*logs):
      sys.stdout.write('\033[F\033[K\033[F\033[K\033[F\033[K')
      originalPrint(*logs)
      originalPrint(self.msg)
      sys.stdout.flush()

    print(f'\033[90m---------- {self.name}\033[0m')
      
    total = len(self.data)
    originalPrint = builtins.print
    builtins.print = newPrint

    self.msg = f'\033[90m----------\nProcessing {self.name}... 0 of {total} (0.00%)\n----------\033[0m'
    originalPrint(self.msg)

    start = time.time()
    for i, item in enumerate(self.data):
      current = i + 1
      elapsedTime = time.time() - start
      remainingTime = (elapsedTime / i) * (total - i) if i > 0 else 0
      perc = f'{((current) / total * 100):.2f}%'
      self.msg = f'\033[90m----------\nProcessing {self.name}... {current} of {total} ({perc}) | Elapsed: {elapsedTime:.4f} sec - Remaining: {remainingTime:.4f} sec\n----------\033[0m'
      sys.stdout.write('\033[F\033[K\033[F\033[K\033[F\033[K')
      originalPrint(self.msg)
      sys.stdout.flush()
      yield item

    elapsedTime = time.time() - start
    builtins.print = originalPrint
    sys.stdout.write('\033[F\033[K\033[F\033[K\033[F\033[K')
    print(f'\033[90m----------\n{self.name} processed {total} items in {elapsedTime:.4f} sec\n----------\033[0m')

    




