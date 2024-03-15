CREATE TABLE if not exists trip_data (
    -- See: https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
    -- Taxicab Technology Service Provider or TPEP
    -- 1= Creative Mobile Technologies, LLC; 2= VeriFone Inc
                                         VendorID bigint,
    -- The date and time when the meter was engaged.
                                         tpep_pickup_datetime timestamp,
    -- The date and time when the meter was disengaged.
                                         tpep_dropoff_datetime timestamp,
    -- The number of passengers in the vehicle. This is a driver-entered value.
                                         passenger_count numeric,
    -- The elapsed trip distance in miles reported by the taximeter.
                                         trip_distance numeric,
    -- The final rate code in effect at the end of the trip.
    --
    -- 1= Standard rate
    -- 2= JFK
    -- 3= Newark
    -- 4= Nassau or Westchester
    -- 5= Negotiated fare
    -- 6= Group ride
                                         RatecodeID numeric,
    -- This flag indicates whether the trip record was held in vehicle memory before sending to the vendor,
    -- aka “store and forward,” because the vehicle did not have a connection to the server.
                                         store_and_fwd_flag string,
    -- TLC Taxi Zone in which the taximeter was engaged
                                         PULocationID bigint,
    -- TLC Taxi Zone in which the taximeter was disengaged
                                         DOLocationID bigint,
    -- A numeric code signifying how the passenger paid for the trip.
    --
    -- 1= Credit card
    -- 2= Cash
    -- 3= No charge
    -- 4= Dispute
    -- 5= Unknown
    -- 6= Voided trip
                                         payment_type bigint,
    -- The time-and-distance fare calculated by the meter.
                                         fare_amount numeric,
    -- Miscellaneous extras and surcharges. Currently, this only includes the 0.50 and 1 rush hour and overnight charges.
                                         extra numeric,
    -- 0.50 MTA tax that is automatically triggered based on the metered rate in use.
                                         mta_tax numeric,
    -- This field is automatically populated for credit card tips. Cash tips are not included.
                                         tip_amount numeric,
    -- The amount of the tolls paid in cash.
                                         tolls_amount numeric,
    -- 0.30 improvement surcharge assessed on hailed trips at the flag drop.
                                         improvement_surcharge numeric,
    -- The total amount charged to passengers. Does not include cash tips.
                                         total_amount numeric,
    -- The 2.75 congestion surcharge is a New York State MTA tax.
                                         congestion_surcharge numeric,
    -- $1.25 for pick up only at LaGuardia Airport and John F. Kennedy International Airport.
                                         airport_fee numeric
) WITH (
      connector='kafka',
      topic='trip_data',
      properties.bootstrap.server='message_queue:29092'
) FORMAT PLAIN ENCODE JSON;