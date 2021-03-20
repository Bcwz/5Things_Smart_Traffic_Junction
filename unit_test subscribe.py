import unittest
import MQTT_Broker as con

class TestStringMethods(unittest.TestCase):

    # Test the trafic light count
    @unittest.skip
    def test_run_traffic(self):
        result = con.traffic_condition(scenario_1)
        self.assertEqual(len(result), 2)
    
 
        
if __name__ == '__main__':
    
    # When one side of the traffic have the length of 7
    scenario_1 = f'{{ "":"{False}", "direction":"north_south" , "eme":{True}}}'

    seenario_1_json = {"enable" : True, "traffic_green": False}

    unittest.main()
    
