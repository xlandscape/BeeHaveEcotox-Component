"""Class definition for the Landscape Model BeeHaveEcotox component."""
import base
import typing
import attrib
import os
import numpy
import shapefile
import math
import shutil
import statistics
import random
import shapely.geometry
import shapely.wkb


class BeeHaveEcotox(base.Component):
    """
    Prepares and runs a BeeHave scenario.
    """

    # VERSION

    # CHANGELOG

    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        """
        Initializes a BeeHave component.

        Args:
            name: The name of the component.
            default_observer: The default observer of the component.
            default_store: The default store of the component.
        """
        if not os.path.exists(os.path.join(os.path.join(__file__, "..", "jdk-24", "lib", "modules"))):
            raise FileNotFoundError(
                "Java runtime not found. Please download https://xlandscape.org/releases/jdk-24-v1.0.zip and extract "
                f"it into {os.path.abspath(os.path.join(os.path.join(__file__, '..')))}."
            )
        super(BeeHaveEcotox, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(
            self,
            (
                base.Input(
                    "ProcessingPath",
                    (attrib.Class(str), attrib.Unit(None), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "Nectar",
                    (
                        attrib.Class(numpy.ndarray),
                        attrib.Unit("L/(m²*d)"),
                        attrib.Scales("space/base_geometry, time/day")
                    ),
                    self.default_observer
                ),
                base.Input(
                    "Pollen",
                    (
                        attrib.Class(numpy.ndarray),
                        attrib.Unit("g/(m²*d)"),
                        attrib.Scales("space/base_geometry, time/day")
                    ),
                    self.default_observer
                ),
                base.Input(
                    "BeeHaveMapCenterPointX",
                    (attrib.Class(float), attrib.Unit("m"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "BeeHaveMapCenterPointY",
                    (attrib.Class(float), attrib.Unit("m"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "SegmentationGridRadii",
                    (attrib.Class(list[float]), attrib.Unit("m"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "SegmentationGridSteps",
                    (attrib.Class(int), attrib.Unit("1"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "SegmentationGridNumberSegmentsPerRadius",
                    (attrib.Class(list[int]), attrib.Unit("1"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "NumberTimeSteps",
                    (attrib.Class(int), attrib.Unit("1"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "Vegetation",
                    (attrib.Class(numpy.ndarray), attrib.Unit(None), attrib.Scales("space/base_geometry")),
                    self.default_observer
                ),
                base.Input(
                    "Vegetation",
                    (attrib.Class(numpy.ndarray), attrib.Unit(None), attrib.Scales("space/base_geometry")),
                    self.default_observer
                ),
                base.Input(
                    "AppliedVegetationId",
                    (attrib.Class(int), attrib.Unit("1"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "MinNumberApplications",
                    (attrib.Class(int), attrib.Unit("1"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "MaxNumberApplications",
                    (attrib.Class(int), attrib.Unit("1"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "FirstDayOfYearApplications",
                    (attrib.Class(int), attrib.Unit("1"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "LastDayOfYearApplications",
                    (attrib.Class(int), attrib.Unit("1"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "ConcNectarMean",
                    (attrib.Class(float), attrib.Unit("µg/kg"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "ConcNectarStd",
                    (attrib.Class(float), attrib.Unit("µg/kg"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "ConcPollenMean",
                    (attrib.Class(float), attrib.Unit("µg/kg"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "ConcPollenStd",
                    (attrib.Class(float), attrib.Unit("µg/kg"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "ContactToxicityMean",
                    (attrib.Class(float), attrib.Unit("kg/ha"), attrib.Scales("global")),
                    self.default_observer,
                    description="Mean application rate of the treated crop in kg a.i./ha, written to the "
                                "ETOX_PPPContact_patch column of Sources.txt. BEEHAVEecotox derives the contact dose "
                                "per bee as rate [kg/ha] * RUD [(ha*mg)/(kg*kg)] * 0.1 g bee weight (RUD is fixed at "
                                "21). It is not a toxicity endpoint."
                ),
                base.Input(
                    "ContactToxicityStd",
                    (attrib.Class(float), attrib.Unit("kg/ha"), attrib.Scales("global")),
                    self.default_observer,
                    description="Standard deviation of the application rate in kg a.i./ha, used to draw a rate per "
                                "treated patch. See ContactToxicityMean."
                ),
                base.Input(
                    "ExposurePeriod",
                    (attrib.Class(int), attrib.Unit("d"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "ResidueUnitDose",
                    (attrib.Class(float), attrib.Unit("(ha*mg)/(kg*kg)"), attrib.Scales("global")),
                    self.default_observer,
                    description="Residue per unit dose (ETOX_RUD) used by BEEHAVEecotox to convert the application "
                                "rate into a contact dose per bee. A value of 0 switches contact exposure off."
                ),
                base.Input(
                    "PlantDT50",
                    (attrib.Class(float), attrib.Unit("d"), attrib.Scales("global")),
                    self.default_observer,
                    description="Whole-plant dissipation half-life of the substance in days (ETOX_DT50); drives the "
                                "decline of nectar and pollen residues after an application."
                ),
                base.Input(
                    "ForagerOralLD50",
                    (attrib.Class(float), attrib.Unit("µg/bee"), attrib.Scales("global")),
                    self.default_observer,
                    description="Acute oral LD50 of adult bees in µg per bee (ETOX_Forager_Oral_LD50)."
                ),
                base.Input(
                    "ForagerOralSlope",
                    (attrib.Class(float), attrib.Unit("1"), attrib.Scales("global")),
                    self.default_observer,
                    description="Slope of the log-logistic oral dose-response curve of adult bees "
                                "(ETOX_Forager_Oral_Slope)."
                ),
                base.Input(
                    "ForagerContactLD50",
                    (attrib.Class(float), attrib.Unit("µg/bee"), attrib.Scales("global")),
                    self.default_observer,
                    description="Acute contact LD50 of adult bees in µg per bee (ETOX_Forager_contact_LD50)."
                ),
                base.Input(
                    "ForagerContactSlope",
                    (attrib.Class(float), attrib.Unit("1"), attrib.Scales("global")),
                    self.default_observer,
                    description="Slope of the log-logistic contact dose-response curve of adult bees "
                                "(ETOX_Forager_contact_Slope)."
                ),
                base.Input(
                    "LarvaeOralLD50",
                    (attrib.Class(float), attrib.Unit("µg/larva"), attrib.Scales("global")),
                    self.default_observer,
                    description="Oral LD50 of larvae in µg per larva (ETOX_Larvae_Oral_LD50)."
                ),
                base.Input(
                    "LarvaeOralSlope",
                    (attrib.Class(float), attrib.Unit("1"), attrib.Scales("global")),
                    self.default_observer,
                    description="Slope of the log-logistic oral dose-response curve of larvae (ETOX_Larvae_Oral_Slope)."
                ),
                base.Input(
                    "RandomSeed",
                    (attrib.Class(int), attrib.Unit("1"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "BeeHaveWeather",
                    (attrib.Class(str), attrib.Unit(None), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "BeeHaveWeatherFile",
                    (attrib.Class(str), attrib.Unit(None), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "JavaMemoryAllocation",
                    (attrib.Class(str), attrib.Unit(None), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "NumberReplicates",
                    (attrib.Class(int), attrib.Unit("1"), attrib.Scales("global")),
                    self.default_observer,
                    description="Number of BEEHAVE replicates run in one BehaviorSpace experiment. Replicate k uses "
                                "RAND_SEED = RandomSeed + MonteCarloIndex * NumberReplicates + k."
                ),
                base.Input(
                    "MonteCarloIndex",
                    (attrib.Class(int), attrib.Unit("1"), attrib.Scales("global")),
                    self.default_observer,
                    description="Index of the outer Monte Carlo run (0-based, $(_MC_ID_) of the framework). Shifts the "
                                "seed block of this run so that application draws and BEEHAVE replicates never repeat "
                                "across Monte Carlo runs."
                ),
                base.Input(
                    "SunshineHours",
                    (attrib.Class(list[float]), attrib.Unit(None), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "SeasonHoPoMoRepX1",
                    (attrib.Class(int), attrib.Unit("1"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "SeasonHoPoMoRepX2",
                    (attrib.Class(int), attrib.Unit("1"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "SeasonHoPoMoRepX3",
                    (attrib.Class(int), attrib.Unit("1"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "SeasonHoPoMoRepX4",
                    (attrib.Class(int), attrib.Unit("1"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "SeasonHoPoMoRepX5",
                    (attrib.Class(int), attrib.Unit("1"), attrib.Scales("global")),
                    self.default_observer
                )
            )
        )

    def run(self) -> None:
        """
        Runs the component.

        Returns:
            Nothing.
        """
        processing_path = self.inputs["ProcessingPath"].read().values
        output_file = os.path.join(processing_path, "output.csv")
        os.makedirs(processing_path)
        base.replace_tokens(
            {
                "SunshineHours": " ".join([str(x) for x in self.inputs["SunshineHours"].read().values]),
                "SeasonHoPoMoRepX1": self.inputs["SeasonHoPoMoRepX1"].read().values,
                "SeasonHoPoMoRepX2": self.inputs["SeasonHoPoMoRepX2"].read().values,
                "SeasonHoPoMoRepX3": self.inputs["SeasonHoPoMoRepX3"].read().values,
                "SeasonHoPoMoRepX4": self.inputs["SeasonHoPoMoRepX4"].read().values,
                "SeasonHoPoMoRepX5": self.inputs["SeasonHoPoMoRepX5"].read().values
            },
            os.path.abspath(os.path.join(__file__, "..", "BEEHAVEEcotox", "A7-ModelCode_BEEHAVE-ECOTOX.nlogo")),
            os.path.join(processing_path, "A7-ModelCode_BEEHAVE-ECOTOX.nlogo")
        )
        number_replicates = self.inputs["NumberReplicates"].read().values
        # Non-overlapping seed block per outer Monte Carlo run: MC m, replicate k -> base + m * n + k.
        random_seed = (
            self.inputs["RandomSeed"].read().values
            + self.inputs["MonteCarloIndex"].read().values * number_replicates
        )
        self._random_seed = random_seed
        weather_mode = self.inputs["BeeHaveWeather"].read().values
        weather_file_input = self.inputs["BeeHaveWeatherFile"].read().values
        weather_file_for_experiment = weather_file_input or "WeatherSite01.txt"
        if weather_mode == "Weather File" and weather_file_input:
            weather_file_source = weather_file_input
            if not os.path.isabs(weather_file_source):
                weather_file_source = os.path.abspath(weather_file_source)
            weather_file_for_experiment = os.path.basename(weather_file_source)
            shutil.copy(weather_file_source, os.path.join(processing_path, weather_file_for_experiment))
        base.replace_tokens(
            {
                "NumberTimeSteps": str(self.inputs["NumberTimeSteps"].read().values),
                "RandomSeed": str(random_seed),
                "RandomSeedLast": str(random_seed + number_replicates - 1),
                "NumberReplicates": str(number_replicates),
                "Weather": weather_mode,
                "WeatherFile": weather_file_for_experiment,
                "PlantDT50": str(self.inputs["PlantDT50"].read().values),
                "ResidueUnitDose": str(self.inputs["ResidueUnitDose"].read().values),
                "ForagerOralLD50": str(self.inputs["ForagerOralLD50"].read().values),
                "ForagerOralSlope": str(self.inputs["ForagerOralSlope"].read().values),
                "ForagerContactLD50": str(self.inputs["ForagerContactLD50"].read().values),
                "ForagerContactSlope": str(self.inputs["ForagerContactSlope"].read().values),
                "LarvaeOralLD50": str(self.inputs["LarvaeOralLD50"].read().values),
                "LarvaeOralSlope": str(self.inputs["LarvaeOralSlope"].read().values),
            },
            os.path.abspath(os.path.join(__file__, "..", "template", "experiment.xml")),
            os.path.join(processing_path, "experiment.xml")
        )
        self.create_forage_input_file(processing_path)
        base.run_process(
            (
                os.path.abspath(os.path.join(__file__, "..", "jdk-24", "bin", "java.exe")),
                f"-Xmx{self.inputs['JavaMemoryAllocation'].read().values}",
                "-Dfile.encoding=UTF-8",
                "-cp",
                os.path.abspath(os.path.join(__file__, '..', 'NetLogo 5.3.1', 'app', 'NetLogo.jar')),
                "org.nlogo.headless.Main",
                "--model",
                "A7-ModelCode_BEEHAVE-ECOTOX.nlogo",
                "--setup-file",
                "experiment.xml",
                "--table",
                output_file
            ),
            processing_path,
            self.default_observer,
            {}
        )

    def create_forage_input_file(self, processing_path: str) -> None:
        """
        Creates a BeeHave forage input file by consolidating the landscape information into a small number of patches.

        Args:
            processing_path: The working directory for the component.

        Returns:
            Nothing.
        """

        def polar_point(origin_point, angle, d):
            """
            Translates polar coordinates of a point into cartesian coordinates.

            Args:
                origin_point: The cartesian coordinates of the polar coordinate system's origin.
                angle: The angle of the polar coordinate point.
                d: The distance of the polar coordinate point.

            Returns:
                A tuple containing the cartesian coordinates of the polar coordinate point.
            """
            return (
                origin_point.x + math.sin(math.radians(angle)) * d,
                origin_point.y + math.cos(math.radians(angle)) * d
            )

        random.seed(self._random_seed)
        vegetation = self.inputs["Vegetation"].read().values
        steps = self.inputs["SegmentationGridSteps"].read().values
        applied_vegetation_id = self.inputs["AppliedVegetationId"].read().values
        min_number_applications = self.inputs["MinNumberApplications"].read().values
        max_number_applications = self.inputs["MaxNumberApplications"].read().values
        first_day_of_year_applications = self.inputs["FirstDayOfYearApplications"].read().values
        last_day_of_year_applications = self.inputs["LastDayOfYearApplications"].read().values
        number_time_steps = self.inputs["NumberTimeSteps"].read().values
        conc_nectar_mean = self.inputs["ConcNectarMean"].read().values
        conc_nectar_std = self.inputs["ConcNectarStd"].read().values
        conc_pollen_mean = self.inputs["ConcPollenMean"].read().values
        conc_pollen_std = self.inputs["ConcPollenStd"].read().values
        contact_toxicity_mean = self.inputs["ContactToxicityMean"].read().values
        contact_toxicity_std = self.inputs["ContactToxicityStd"].read().values
        exposure_period = self.inputs["ExposurePeriod"].read().values
        residue_unit_dose = self.inputs["ResidueUnitDose"].read().values
        step_angle_width = 360 / steps
        segments_output_file = os.path.join(processing_path, "segments.shp")
        w = shapefile.Writer(segments_output_file, shapefile.POLYGON)
        w.field("ID", "I")
        radii = self.inputs["SegmentationGridRadii"].read().values
        segments = self.inputs["SegmentationGridNumberSegmentsPerRadius"].read().values
        if len(segments) != len(radii):
            raise ValueError("Number of segments and radii do not match.")
        center = shapely.geometry.Point(
            self.inputs["BeeHaveMapCenterPointX"].read().values, self.inputs["BeeHaveMapCenterPointY"].read().values)
        nectar = self.inputs["Nectar"].read()
        pollen = self.inputs["Pollen"].read()
        if nectar.geometries[0].store_name != pollen.geometries[0].store_name:
            raise ValueError("Geometries of nectar and pollen differ.")
        if nectar.values.shape != pollen.values.shape:
            raise ValueError("Shapes of nectar and pollen differ.")
        consolidated_output_file = os.path.join(processing_path, "consolidated.shp")
        patches = [shapely.wkb.loads(x).buffer(0) for x in nectar.geometries[0].get_values()]
        output_file = os.path.join(processing_path, "Sources.txt")
        output_applications = os.path.join(processing_path, "applications.txt")
        i = 1
        for radius_id in range(0, len(radii)):
            for segment in range(segments[radius_id]):
                segment_vertices = []
                if radius_id == 0:
                    for z in range(steps):
                        segment_vertices.append(polar_point(center, z * step_angle_width, radii[radius_id]))
                else:
                    for z in range(0, int(360 / segments[radius_id]) + 1):
                        segment_vertices.append(
                            polar_point(
                                center, z * step_angle_width + segment * 360 / segments[radius_id], radii[radius_id]))
                    for z in range(int(360 / segments[radius_id]), -1, -1):
                        segment_vertices.append(polar_point(
                            center, z * step_angle_width + segment * 360 / segments[radius_id], radii[radius_id - 1]))
                w.poly([segment_vertices])
                w.record(i)
                i += 1
        w.close()
        segment_sf = shapefile.Reader(segments_output_file)
        segment_polygons = [shapely.geometry.Polygon(x.points) for x in segment_sf.shapes()]
        w = shapefile.Writer(consolidated_output_file, shapefile.POINT)
        w.field("ID", "N", 10)
        w.field("VEG_TYPE")
        w.field("AREA", "N", 10, 2)
        w.field("APPLIED", "N", 1)
        # DBF has a hard cap on fields; serialize one-year forage windows for source generation.
        forage_days = min(365, pollen.values.shape[1])
        for attribute in ("NECTAR", "POLLEN"):
            for day in range(forage_days):
                w.field(f"{attribute}_{day}", "N", 10, 4)
        patch_types = {}
        patch_station_mapping = {}
        station_id = 0
        for segment in segment_polygons:
            type_dictionary = {}
            intersection_dictionary = {}
            for patch in range(len(patches)):
                if (
                        numpy.count_nonzero(nectar.values[patch]) + numpy.count_nonzero(pollen.values[patch]) > 0 and
                        numpy.count_nonzero(numpy.isnan(nectar.values[patch])) +
                        numpy.count_nonzero(numpy.isnan(pollen.values[patch])) == 0
                ):
                    if segment.intersects(patches[patch]):
                        patch_applied = vegetation[patch] == applied_vegetation_id
                        patch_type = hash(
                            numpy.append(
                                nectar.values[patch],
                                numpy.append(pollen.values[patch], numpy.array([patch_applied * 1.], ))
                            ).tobytes()
                        )
                        if patch_type not in patch_types:
                            patch_types[patch_type] = {
                                "nectar": nectar.values[patch],
                                "pollen": pollen.values[patch],
                                "label": str(len(patch_types) + 1),
                                "applied": patch_applied
                            }
                        intersection = patches[patch].intersection(segment)
                        if not intersection.is_empty:
                            if patch_type in type_dictionary:
                                type_dictionary[patch_type] = type_dictionary[patch_type].union(intersection)
                            else:
                                type_dictionary[patch_type] = patches[patch].intersection(intersection)
                            intersection_dictionary.setdefault(patch_type, []).append((patch, intersection.area))
            for key in type_dictionary:
                centroid = type_dictionary[key].centroid
                w.point(centroid.x, centroid.y)
                area = type_dictionary[key].area
                values = {
                    "ID": station_id,
                    "VEG_TYPE": patch_types[key]["label"],
                    "AREA": area,
                    "APPLIED": patch_types[key]["applied"] * 1
                }
                for attribute in ("NECTAR", "POLLEN"):
                    for day in range(forage_days):
                        values[f"{attribute}_{day}"] = patch_types[key][attribute.lower()][day] * area
                w.record(**values)
                for patch_intersection in intersection_dictionary[key]:
                    mapping = patch_station_mapping.setdefault(
                        patch_intersection[0],
                        (station_id, patch_intersection[1])
                    )
                    if patch_intersection[1] > mapping[1]:
                        patch_station_mapping[patch_intersection[0]] = (station_id, patch_intersection[1])
                station_id += 1
        w.close()
        sf = shapefile.Reader(consolidated_output_file)
        points = sf.shapeRecords()
        station_patch_mapping = {}
        patch_names = nectar.element_names[0].get_values()
        for k, v in patch_station_mapping.items():
            station_patch_mapping.setdefault(v[0], []).append(patch_names[k])
        with (open(output_file, "w") as f, open(output_applications, "w") as f2):
            f.write(
                "ID\toldPatchID\tpatchType\tdistance_m\txcor\tycor\tsize_sqm\tquantityPollen_g\tConcentration\t"
                "quantityNectar_l\tcalcDetectProb\tmodelDetectProb\tNectarGathering_s\tPollenGathering_s\t"
                "startDay\tstopDay\tETOX_ApplicationList_patch\tETOX_ExposurePeriodsList_patch\t"
                "ETOX_PPPConcNectar_patch\tETOX_PPPConcPollen_patch\tETOX_PPPContact_patch\tETOX_WaterVolume_patch\t"
                "ETOX_WaterConc_patch\tETOX_RUD_patch\n"
            )
            # noinspection SpellCheckingInspection
            f2.write("lulc_feature_id,application_day,conc_nectar,conc_pollen,contact\n")
            nectar_start_col = 4
            pollen_start_col = nectar_start_col + forage_days
            nectar_end_col = nectar_start_col + forage_days - 1
            pollen_end_col = pollen_start_col + forage_days - 1
            day_offset = nectar_start_col - 3
            for i, point in enumerate(points):
                distance = math.sqrt(
                    math.pow(
                        center.x - point.shape.points[0][0], 2.0) + math.pow(center.y - point.shape.points[0][1], 2.0))
                if round(distance, 2) > 0:
                    first_index_nectar = 0
                    last_index_nectar = 0
                    first_index_pollen = 0
                    last_index_pollen = 0
                    for index in range(nectar_start_col, nectar_end_col + 1):
                        if point.record[index] > 0:
                            first_index_nectar = index
                            break
                    for index in range(nectar_end_col, nectar_start_col - 1, -1):
                        if point.record[index] > 0:
                            last_index_nectar = index
                            break
                    for index in range(pollen_start_col, pollen_end_col + 1):
                        if point.record[index] > 0:
                            first_index_pollen = index
                            break
                    for index in range(pollen_end_col, pollen_start_col - 1, -1):
                        if point.record[index] > 0:
                            last_index_pollen = index
                            break
                    if all(
                            (
                                    first_index_pollen > 0,
                                    last_index_pollen > 0,
                                    first_index_nectar > 0,
                                    last_index_nectar > 0
                            )
                    ):
                        first_day_flowering = min(
                            first_index_nectar - day_offset,
                            first_index_pollen - (pollen_start_col - 3)
                        )
                        last_day_flowering = max(
                            last_index_nectar - day_offset,
                            last_index_pollen - (pollen_start_col - 3)
                        )
                        nectar = statistics.mean(
                            point.record[
                                first_day_flowering + day_offset:last_day_flowering + day_offset
                            ]
                        )
                        pollen = statistics.mean(
                            point.record[
                                first_day_flowering + (pollen_start_col - 3):last_day_flowering + (pollen_start_col - 3)
                            ]
                        )
                        f.write(
                            f"{point.record['ID']}\t{point.record['ID']}\t{int(float(point.record['VEG_TYPE']))}\t"
                            f"{format(distance, 'f')}\t{format(center.x - point.shape.points[0][0], 'f')}\t"
                            f"{format(center.y - point.shape.points[0][1], 'f')}\t{format(point.record['AREA'], 'f')}\t"
                            f"{format(pollen, 'f')}\t1.5\t{format(nectar, 'f')}\t"
                            f"{format(1 / distance * math.sqrt(point.record['AREA']) / 100, 'f')}\t-999\t1200\t600\t"
                        )
                        number_applications = random.randint(
                            min_number_applications,
                            max_number_applications
                        ) * point.record["APPLIED"]
                        if number_applications > 0:
                            applications = []
                            for year_start in range(0, number_time_steps, 365):
                                year_end = min(year_start + 365, number_time_steps)
                                # Use configured day-of-year window when possible. If the
                                # simulation chunk is shorter than that window (e.g. 90-day
                                # runs with first_day_of_year_applications=100), fall back to
                                # the full available chunk to guarantee valid application days.
                                year_window_start = year_start + first_day_of_year_applications
                                year_window_end = min(year_start + last_day_of_year_applications, year_end)
                                if year_window_start > year_window_end:
                                    year_window_start = year_start + 1
                                    year_window_end = year_end
                                applications.extend(
                                    random.randint(year_window_start, year_window_end)
                                    for _ in range(number_applications)
                                )
                            applications.sort()
                            conc_nectar = random.normalvariate(conc_nectar_mean, conc_nectar_std)
                            conc_pollen = random.normalvariate(conc_pollen_mean, conc_pollen_std)
                            contact = random.normalvariate(contact_toxicity_mean, contact_toxicity_std)
                            f.write(
                                f"{first_day_flowering}\t{last_day_flowering}\t"
                                f"[{' '.join([str(x) for x in applications])}]\t"
                                f"[{exposure_period}]\t"
                                f"{conc_nectar}\t{conc_pollen}\t{contact}\t"
                                f"10000\t0\t{residue_unit_dose}\n"
                            )
                            for feature in station_patch_mapping.get(point.record["ID"], []):
                                for application in applications:
                                    f2.write(f"{feature},{application},{conc_nectar},{conc_pollen},{contact}\n")
                        else:
                            f.write(f"{first_day_flowering}\t{last_day_flowering}\t[]\t[]\t0\t0\t0\t10000\t0\t0\n")
