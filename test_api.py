import requests
import unittest

PORT=4000

class ApiTest(unittest.TestCase):
    
    # Make sure it doesn't break when given a GET request
    def test1(self):
        res = requests.get('http://localhost:'+str(PORT)+'/Calender')
        self.assertEqual(res.text, 'No Date Argument', msg='Test 1 failed')

    # Make sure the expected case works
    def test2(self):
        res = requests.get('http://localhost:'+str(PORT)+'/Calender?date=05/12/2019')
        self.assertEqual(res.status_code, 200 , msg='Test 2 failed')

    # Make sure if the user forgets preceeding 0's it works
    def test3(self):
        res = requests.get('http://localhost:'+str(PORT)+'/Calender?date=5/12/2019')
        self.assertEqual(res.status_code, 200 , msg='Test 3.1 failed')
        res = requests.get('http://localhost:'+str(PORT)+'/Calender?date=05/7/2019')
        self.assertEqual(res.status_code, 200 , msg='Test 3.2 failed')
        res = requests.get('http://localhost:'+str(PORT)+'/Calender?date=5/7/2019')
        self.assertEqual(res.status_code, 200 , msg='Test 3.3 failed')

    # Make sure if there is no date field we don't crash
    def test4(self):
        res = requests.get('http://localhost:'+str(PORT)+'/Calender?ar1=abc')
        self.assertEqual(res.text, 'No Date Argument' , msg='Test 4 failed')
        
    # Make sure if the date field is empty we return error
    def test5(self):
        res = requests.get('http://localhost:'+str(PORT)+'/Calender?date=')
        self.assertEqual(res.text, 'Date Argument Empty' , msg='Test 5.1 failed')
        res = requests.get('http://localhost:'+str(PORT)+'/Calender?date')
        self.assertEqual(res.text, 'Date Argument Empty' , msg='Test 5.2 failed')

    #Make sure it doesn't allow invalid dates
    def test6(self):
        res = requests.get('http://localhost:'+str(PORT)+'/Calender?date=999/9999')
        self.assertEqual(res.text, 'Invalid Date Format' , msg='Test 6.1 failed')
        res = requests.get('http://localhost:'+str(PORT)+'/Calender?date=999/9999/99999')
        self.assertEqual(res.text, 'Invalid Date' , msg='Test 6.2 failed')
        res = requests.get('http://localhost:'+str(PORT)+'/Calender?date=99/99/9999')
        self.assertEqual(res.text, 'Invalid Date' , msg='Test 6.3 failed')
        res = requests.get('http://localhost:'+str(PORT)+'/Calender?date=-1/12/2003')
        self.assertEqual(res.text, 'Invalid Date' , msg='Test 6.4 failed')
        res = requests.get('http://localhost:'+str(PORT)+'/Calender?date=01/-22/2019')
        self.assertEqual(res.text, 'Invalid Date' , msg='Test 6.5 failed')
        res = requests.get('http://localhost:'+str(PORT)+'/Calender?date=01/12/-1000')
        self.assertEqual(res.text, 'Invalid Date' , msg='Test 6.6 failed')
        res = requests.get('http://localhost:'+str(PORT)+'/Calender?date=aa/b/1000')
        self.assertEqual(res.text, 'Invalid Date' , msg='Test 6.7 failed')
        res = requests.get('http://localhost:'+str(PORT)+'/Calender?date=a/d/c')
        self.assertEqual(res.text, 'Invalid Date' , msg='Test 6.8 failed')

if __name__ == '__main__':
    unittest.main()

