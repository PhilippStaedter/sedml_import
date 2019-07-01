# set time data for special models from BioModels-Database

def timePointsBioModels(iModel):

    if iModel == 'Bungay2003':
        sim_start_time = 0
        sim_end_time = 500                  #0.2
        sim_num_time_points = 1000

    elif iModel == 'Bungay2006':
        sim_start_time = 0
        sim_end_time = 500
        sim_num_time_points = 1000

    elif iModel == 'Bungay2006a':
        sim_start_time = 0
        sim_end_time = 500                  #2
        sim_num_time_points = 1000

    elif iModel == 'Eungdamrong2007':
        sim_start_time = 0
        sim_end_time = 30000
        sim_num_time_points = 50

    elif iModel == 'Froehlich2018':
        sim_start_time = 0
        sim_end_time = 100000000
        sim_num_time_points = 2

    elif iModel == 'Holzhutter2004':
        sim_start_time = 0
        sim_end_time = 0.00001
        sim_num_time_points = 50

    elif iModel == 'Hui2014':
        sim_start_time = 0
        sim_end_time = 1000
        sim_num_time_points = 50

    elif iModel == 'Lai2014':
        sim_start_time = 0
        sim_end_time = 1
        sim_num_time_points = 50

    elif iModel == 'Leber2015':
        sim_start_time = 0
        sim_end_time = 70
        sim_num_time_points = 50

    elif iModel == 'Levchenko2000a':
        sim_start_time = 0
        sim_end_time = 500
        sim_num_time_points = 1000

    elif iModel == 'Liu2011':
        sim_start_time = 0
        sim_end_time = 20000
        sim_num_time_points = 1000

    elif iModel == 'Nakakuki2010':
        sim_start_time = 0
        sim_end_time = 5500
        sim_num_time_points = 1000

    elif iModel == 'ODea2007':
        sim_start_time = 0
        sim_end_time = 4000
        sim_num_time_points = 50

    elif iModel == 'Ouzounoglou2014':
        sim_start_time = 0
        sim_end_time = 600000
        sim_num_time_points = 50

    elif iModel == 'Pathak2013':
        sim_start_time = 0
        sim_end_time = 150
        sim_num_time_points = 50

    elif iModel == 'Pathak2013a':
        sim_start_time = 0
        sim_end_time = 120
        sim_num_time_points = 50

    elif iModel == 'Pritchard2002':
        sim_start_time = 0
        sim_end_time = 1
        sim_num_time_points = 50

    elif iModel == 'Proctor2010a':
        sim_start_time = 0
        sim_end_time = 15000000
        sim_num_time_points = 50

    elif iModel == 'Proctor2013a':
        sim_start_time = 0
        sim_end_time = 15000000
        sim_num_time_points = 50

    elif iModel == 'Qi2013a':
        sim_start_time = 0
        sim_end_time = 15000000
        sim_num_time_points = 50

    elif iModel == 'Sasagawa2005':
        sim_start_time = 0
        sim_end_time = 6000
        sim_num_time_points = 50

    elif iModel == 'Sengupta2015':
        sim_start_time = 0
        sim_end_time = 0.08
        sim_num_time_points = 50

    elif iModel == 'Singh2006':
        sim_start_time = 0
        sim_end_time = 700000
        sim_num_time_points = 50

    elif iModel == 'Sivakumar2011c':
        sim_start_time = 0
        sim_end_time = 2000
        sim_num_time_points = 50

    elif iModel == 'Ueda2001':
        sim_start_time = 0
        sim_end_time = 72
        sim_num_time_points = 50

    elif iModel == 'Ung2008':
        sim_start_time = 0
        sim_end_time = 2000
        sim_num_time_points = 50

    elif iModel == 'Yang2007':
        sim_start_time = 0
        sim_end_time = 300000
        sim_num_time_points = 50


    return sim_start_time, sim_end_time, sim_num_time_points