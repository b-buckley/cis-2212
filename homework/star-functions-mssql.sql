
-- I want to create a view that, for each observation, lists the observed star and the altitude
-- the star was above the horizon at the time it was observed. Researchers may want to filter
-- out observations done at too low an altitude since such observations might be unreliable.

-- The following three functions compute the local sidereal time from the location of an
-- observer, the date of an observation, and the universal time when that observation is made.
-- Reference: "Astronomical Algorithms", second edition, by Jean Meeus, copyright 1998,
-- published by Willmann-Bell, ISBN=0-9943396-61-1.

-- Compute the Julian day number for 0h UTC on the Gregorian date given.
CREATE FUNCTION JulianDay(
        @Y integer, @M integer, @D integer) RETURNS float AS
BEGIN
  DECLARE @Year  integer = @Y;
  DECLARE @Month integer = @M;
  DECLARE @Day   integer = @D;
  DECLARE @A     integer;
  DECLARE @B     integer;

  IF @Month <= 2
    BEGIN
      SET @Year = @Year - 1;
      SET @Month = @Month + 12;
    END;
  SET @A = @Year/100;
  SET @B = 2 - @A + (@A/4);
  RETURN floor(365.25 * (@Year + 4716)) + floor(30.6001 * (@Month + 1)) + @Day + @B - 1524.5;
END;
GO

-- Compute the sidereal time at the prime meridian for the date/time given. The return value is
-- given in degrees (24 hours = 360 degrees).
CREATE FUNCTION SiderealTime(
        @Year integer, @Month  integer, @Day    integer,
        @Hour integer, @Minute integer, @Second integer) RETURNS float AS
BEGIN
  DECLARE @T       float;
  DECLARE @Theta_0 float;
  DECLARE @Theta   float;

  SET @T = (dbo.JulianDay(@Year, @Month, @Day) - 2451545.0)/36525.0;
  SET @Theta_0 = 100.46061837 + 36000.770053608*@T + 0.000387933*@T*@T + (@T*@T*@T)/38710000.0;
  SET @Theta = 1.00273790935*360.0*((@Second + 60.0*(@Minute + 60.0*@Hour))/86400);
  SET @Theta = @Theta + @Theta_0;
  WHILE @Theta > 360.0
    BEGIN
      SET @Theta = @Theta - 360.0;
    END;
  RETURN @Theta;
END;
GO

-- Compute the sidereal time at a specific longitude on the earth. The return value is given in
-- degrees (24 hours = 360 degrees).
CREATE FUNCTION LocalSiderealTime(
        @Year  integer, @Month  integer, @Day    integer,
        @Hour  integer, @Minute integer, @Second integer,
        @Longitude float) returns float AS
BEGIN
  DECLARE @Prime_Time float = dbo.SiderealTime(@Year, @Month, @Day, @Hour, @Minute, @Second);
  RETURN @Prime_Time + @Longitude;
END;
GO


-- Compute the altitude of a spot on the sky at a place and time. The return value is given in
-- degrees. I should probably introduce some structured types to clean up this long parameter
-- list.
CREATE FUNCTION Altitude(
        -- The time...
        @Year  integer, @Month  integer, @Day    integer,
        @Hour  integer, @Minute integer, @Second integer,

        -- The place...
        @Longitude float,
        @Latitude float,

        -- The position on the sky...
        @RA float,
        @Declination float) returns float AS
BEGIN
  DECLARE @LST float = dbo.LocalSiderealTime(
    @Year, @Month, @Day, @Hour, @Minute, @Second, @Longitude);
  DECLARE @Right_Ascension float = 360.0*(@RA/24.0);

  DECLARE @Pole_Zenith float;  -- Distance from pole to zenith.
  DECLARE @Pole_Star   float;  -- Distance from pole to star.
  DECLARE @Zenith_Star float;  -- Distance from zenith to star.
  DECLARE @RA_Diff     float;  -- Different between RA and local sidereal time.

  -- This computation involves spherical trigonometry (rule of cosines).
  SET @Pole_Zenith = 90.0 - @Latitude;
  SET @Pole_Star   = 90.0 - @Declination;
  SET @RA_Diff     = @Right_Ascension - @LST;

  -- Convert to radians.
  SET @Pole_Zenith = (@Pole_Zenith/360.0) * 2.0 * 3.14159;
  SET @Pole_Star   = (@Pole_Star/360.0) * 2.0 * 3.14159;
  SET @RA_Diff     = (@RA_Diff/360.0) * 2.0 * 3.14159;

  -- Compute the interesting angle.
  SET @Zenith_Star = acos(cos(@Pole_Zenith) * cos(@Pole_Star) +
                          sin(@Pole_Zenith) * sin(@Pole_Star) * cos(@RA_Diff));

  -- Convert back to degrees.
  SET @Zenith_Star = 360.0 * @Zenith_Star/(2.0 * 3.14159);
  
  RETURN 90.0 - @Zenith_Star;
END;
GO


-- Create the desired view. Researchers can join this view against OBSERVATION to look up other
-- details about an observation once it passes altitude criteria.
CREATE VIEW star_altitudes AS
        SELECT ob.id as observation_id, ob.name, ob.const, dbo.Altitude(
          ob.year,    ob.month,   ob.day,     ob.hour,   ob.minute,  0,
          l.longitude, l.latitude,
          s.ra, s.dec) AS altitude
        FROM OBSERVATION ob, LOCATION l, STAR s
        WHERE ob.location_id = l.id AND
              ob.name  = s.name     AND
              ob.const = s.const;
GO
