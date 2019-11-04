
polar_idx={'positive': 0, 'negative': 1, 'neutral': 2}

idx_polar={0: 'positive', 1: 'negative', 2: 'neutral'}

file_config = {
    '14': {
        'laptop': {
            'train': 'Laptop_Train_v2.xml', 
            'test': 'Laptops_Test_Gold.xml'
        },
        'rest': {
            'train': 'Restaurants_Train_v2.xml',
            'test': 'Restaurants_Test_Gold.xml'
        }
    },

    '15': {
        'laptop': {
            'train': 'ABSA-15_Laptops_Train_Data.xml', 
            'test': 'ABSA15_Laptops_Test.xml'
        },
        'rest': {
            'train': 'ABSA-15_Restaurants_Train_Final.xml',
            'test': 'ABSA15_Restaurants_Test.xml'
        }
    },

    '16': {
        'laptop': {
            'train': 'ABSA16_Laptops_Train_SB1_v2.xml', 
            'test': 'EN_LAPT_SB1_TEST_.xml.gold'
        },
        'rest': {
            'train': 'ABSA16_Restaurants_Train_SB1_v2.xml',
            'test': 'EN_REST_SB1_TEST.xml.gold'
        }
    }
}
