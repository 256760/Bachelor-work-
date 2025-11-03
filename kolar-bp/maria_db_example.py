from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, selectinload, load_only
import math

from chmi_metadata_models import WeatherStation
from config import CHMI_METADATA_CONNECTION_STRING, CML_METADATA_CONNECTION_STRING

chmi_metadata_engine = create_engine(CHMI_METADATA_CONNECTION_STRING)
chmi_metadata_session = Session(chmi_metadata_engine)

cml_metadata_engine = create_engine(CML_METADATA_CONNECTION_STRING)
cml_metadata_session = Session(cml_metadata_engine)


from cml_metadata_models import Link, Technology, Site

stations = chmi_metadata_session.scalars(
    select(WeatherStation)
    .join(WeatherStation.measurements_10m)
    .options(selectinload(WeatherStation.measurements_10m) )
    #.distinct()
)


cmw_query =(
       select(WeatherStation)
       .options(
                load_only(WeatherStation.X, WeatherStation.Y, WeatherStation.full_name),
       )
)

cml_query = (
    select(Link)
    .join(Link.technology)  # join with Technology
    .join(Technology.influx_mapping)  # join with TechnologiesInfluxMapping
    .options(
        selectinload(Link.technology).selectinload(Technology.influx_mapping),
        selectinload(Link.site_A),
        selectinload(Link.site_B),
    )

)

links = cml_metadata_session.scalars(cml_query).all()
stations = chmi_metadata_session.scalars(cmw_query).all()

# for station in stations:

   


# example output
for link in links:

            tech = link.technology
            influx = tech.influx_mapping

         
            # link
            link_site_A = link.site_A       # x = šířka == longtitude
            link_site_B = link.site_B       #y = délka  == longtitude
            link_site_A_ID = link.site_A_id 
            link_site_B_ID = link.site_B_id
            link_distance = link.distance
            link_id = link.id

            if link_distance is not None and link_distance > 2000:
                # print(link_site_A.x_coordinate, link_site_A.y_coordinate)
                # print(link_site_B.x_coordinate, link_site_B.y_coordinate)
                print(f"distance: {link_distance}")
                print(f"link id: {link_id}")
                #print(f"Označení tratě {link_id}, {link_site_A_ID}, {link_site_B_ID}")
                max_distance = 20

                x_start, y_start = 0, 0
                x_end = (link_site_B.x_coordinate - link_site_A.x_coordinate) * math.cos(math.radians(link_site_A.y_coordinate)) * 111
                y_end = (link_site_B.y_coordinate - link_site_A.y_coordinate) * 111

                
                for station in stations:
                        
                    print("x_end:",x_end, "y_end", y_end)


                    station_X_position = station.X
                    station_Y_position = station.Y
                    Station_name = station.full_name   

                    print(station_X_position, station_Y_position, Station_name)

                            
                    x_city = (station_X_position - link_site_A.x_coordinate) * math.cos(math.radians(link_site_A.y_coordinate)) * 111
                    y_city = (station_Y_position - link_site_A.y_coordinate) * 111

                    print("X",x_city,"Y", y_city)

                    #test prints
                    
                    t = ((x_city - x_start)*(x_end - x_start) + (y_city - y_start)*(y_end - y_start)) / ((x_end - x_start)**2 + (y_end - y_start)**2)

                    print("t",t)
                    print("")
                    if t < 0:
                        d_min = math.sqrt((x_city - x_start)**2 + (y_city - y_start)**2)
                        print("t < ",d_min)
                    elif t > 1:
                        d_min = math.sqrt((x_city - x_end)**2 + (y_city - y_end)**2)
                        print("t > ",d_min)
                    else:
                        d_min = abs((y_end - y_start)*x_city - (x_end - x_start)*y_city) / math.sqrt((y_end - y_start)**2 + (x_end - x_start)**2)
                        print("0 ≤ t ≤ 1",d_min)

                if d_min <= max_distance:
                    station_name_distance = {Station_name: d_min}
                    print(f"{station_name_distance} leží poblíž spoje.")

    
            



        #original code

        # print(f"Link {link.id} ({link.ip_address_A} -- {link.ip_address_B})")
        # print(link_site_A.x_coordinate, link_site_A.y_coordinate)
        # print(link_site_B.x_coordinate, link_site_B.y_coordinate)
        # print(f"distance: {distance}")
        #     print("")
            # print(f"menší: {azimuth_A}, azimuth B: {azimuth_B}")
            # print("")
            # print(
            #     f"RSL field: {influx.rsl_field}, TSL field: {influx.tsl_field}, Temp field: {influx.temperature_field}"
            # )
            # print(f"Measurement: {influx.measurement} \n")



     