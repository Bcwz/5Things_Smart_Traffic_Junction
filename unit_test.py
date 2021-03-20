import unittest
import MQTT_Broker as con

class TestStringMethods(unittest.TestCase):

    # Test the trafic light count
    @unittest.skip
    def test_run_traffic(self):
        result = con.traffic_condition(scenario_1)
        self.assertEqual(len(result), 2)
    
    # Test if the string is converted to array
    @unittest.skip
    def test_convert_array(self):
        result = con.traffic_condition(scenario_1)
        
        self.assertEqual(len(result), 3)
    
    # Test if the horizontal side have emergency vehicle
    # @unittest.skip
    def test_check_emergency_vehicle(self):
        msg = con.string_to_json(scenario_1)
        
        result = con.traffic_condition(msg)
        
        self.assertTrue(result)
        
    # Test if the vertical side have emergency vehicle
    @unittest.skip
    def test_check_emergency_vehicle(self):
        result = con.traffic_condition(scenario_3)
        self.assertTrue(result)
    
    # Test if the car length is more than 7
    # If it is vertical it should be true
    # else horizontal is set to true
    @unittest.skip
    def test_length_vertical(self):
        # Testing if it is the vertical
        result = con.traffic_condition(scenario_1)
        self.assertTrue(result)

    @unittest.skip
    def test_json_to_string(self):
        # Testing if it is the vertical
        result = con.string_to_json(scenario_1)
        self.assertEqual(result["traffic_green"], "False")

    @unittest.skip
    def test_string_to_json(self):
        # Testing if it is the vertical
        result = con.json_to_string(seenario_1_json)
        self.assertTrue(bool(result))
    
    
    def test_added_message(self):
        result = con.string_to_json(sub)
        
        
if __name__ == '__main__':
    
    # When one side of the traffic have the length of 7
    sub = f'{{ "direction":"north", "time_left":7 }}'
    
    pub = f'{{ "direction":"north", "enable": true }}'

    seenario_1_json = {"enable" : True, "traffic_green": False}
    # When one side of the traffic have the length of 7
    scenario_2 = f"messages:[{7}, 'east', {False}]"
    
    # When the vertical side have emergency vehicle
    scenario_3 = f"messages:[{3}, 'north', {True}]"
    
    # When the horizontal side have emergency vehicle
    scenario_4 = f"messages:[{3}, 'south', {True}]"


    
    # # When one side have the ambulance
    # scenario_2 = f"messages:{[4, "traffic_north", true ]}"
    
    # # When one side have 7 and have emergency vehicle
    # scenario_3 = f"messages:{[7, "traffic_east", true ]}"
    
    # # When both side of the traffic have a length of 7
    # # Take in scenerio 4 and 1
    # scenario_4 = f"messages:{[7, "traffic_south", false ]}"
    
    # # When both side have 7 car and north have an ambulance
    # # Take in scenerio 5 and scenerio 2
    # scenario_5 = f"messages:{[7, "traffic_south", false ]}"
    
    unittest.main()
    
