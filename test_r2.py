#!/usr/bin/python
import time, csv, logging, sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filename='test.log',level=logging.INFO)

driver = webdriver.Chrome()
driver.get("http://www.thecalculatorsite.com/finance/calculators/loancalculator.php")

### Objects identification
#=========================
select_currency =	Select(driver.find_element(By.XPATH, '//*[@id="currency"]'))
edit_amount =		driver.find_element(By.XPATH, '//*[@id="amount"]')
edit_interest_rate =	driver.find_element(By.XPATH, '//*[@id="percent"]')
edit_months =		driver.find_element(By.XPATH, '//*[@id="term"]')
button_submit =		driver.find_element(By.XPATH, '//*[@id="loanForm"]/div[9]/input')
label_total_pay_xpath = '//*[@id="results1"]/span[4]/b'

### Functional test cases
#========================
def execute_test(data_row):
  logging.info("Running test with the following data curr:"+data_row[0]+", amount:"+data_row[1]+", IR:"+data_row[2]+", months:"+data_row[3]+", total_pay:"+data_row[4])
  
  ### Navigation	
  select_currency.select_by_value(data_row[0])
  edit_amount.send_keys(data_row[1])
  edit_interest_rate.send_keys(data_row[2])
  edit_months.send_keys(data_row[3])
  driver.execute_script("window.scrollTo(0, 0);")
  button_submit.click()
  time.sleep(2)

  ### Assertion
  try:
    total_pay = driver.find_element(By.XPATH, label_total_pay_xpath).text[1:]
    assert total_pay == data_row[4]
    logging.info("Test case PASSED, assertion successful")
  except AssertionError:
    print "Test case FAILED, see the log"
    logging.info("Test case FAILED, assertion unsuccessful, comparing: "+total_pay+ " with " + data_row[4])
    sys.exit(1)
  return

def cleanup():
  edit_amount.clear()
  edit_interest_rate.clear()
  edit_months.clear()
  logging.info("Fields cleaned up")
  return

def import_test_data(file_path):
  with open(file_path, 'rb') as f:
    reader=csv.reader(f)
    test_data=list(reader)
  logging.info("CSV file imported")
  return test_data

if __name__ == '__main__':
  data=import_test_data('./data.csv')
  number_rows=len(data)
  try:
    for row in data:
      execute_test(row)
      cleanup()
      time.sleep(1)
  except IndexError:
    print "End of the data source file reached, closing the test"
