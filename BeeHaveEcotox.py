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
                    (attrib.Class(float), attrib.Unit("µg/bee"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "ContactToxicityStd",
                    (attrib.Class(float), attrib.Unit("µg/bee"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "ExposurePeriod",
                    (attrib.Class(int), attrib.Unit("d"), attrib.Scales("global")),
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
        shutil.copy(
            os.path.abspath(
                os.path.join(__file__, "..", "BEEHAVEEcotox", "A7-ModelCode_BEEHAVE-ECOTOX.nlogo")),
            processing_path
        )
        base.replace_tokens(
            {
                "NumberTimeSteps": str(self.inputs["NumberTimeSteps"].read().values),
                "RandomSeed": 1
            },
            os.path.abspath(os.path.join(__file__, "..", "template", "experiment.xml")),
            os.path.join(processing_path, "experiment.xml")
        )
        self.create_forage_input_file(processing_path)
        base.run_process(
            (
                os.path.abspath(os.path.join(__file__, "..", "jdk-24", "bin", "java.exe")),
                "-Xmx1024m",
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

        vegetation = self.inputs["Vegetation"].read().values
        steps = self.inputs["SegmentationGridSteps"].read().values
        applied_vegetation_id = self.inputs["AppliedVegetationId"].read().values
        min_number_applications = self.inputs["MinNumberApplications"].read().values
        max_number_applications = self.inputs["MaxNumberApplications"].read().values
        first_day_of_year_applications = self.inputs["FirstDayOfYearApplications"].read().values
        last_day_of_year_applications = self.inputs["LastDayOfYearApplications"].read().values
        conc_nectar_mean = self.inputs["ConcNectarMean"].read().values
        conc_nectar_std = self.inputs["ConcNectarStd"].read().values
        conc_pollen_mean = self.inputs["ConcPollenMean"].read().values
        conc_pollen_std = self.inputs["ConcPollenStd"].read().values
        contact_toxicity_mean = self.inputs["ContactToxicityMean"].read().values
        contact_toxicity_std = self.inputs["ContactToxicityStd"].read().values
        exposure_period = self.inputs["ExposurePeriod"].read().values
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
        for attribute in ("NECTAR", "POLLEN"):
            for day in range(pollen.values.shape[1]):
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
                    for day in range(pollen.values.shape[1]):
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
            for i, point in enumerate(points):
                distance = math.sqrt(
                    math.pow(
                        center.x - point.shape.points[0][0], 2.0) + math.pow(center.y - point.shape.points[0][1], 2.0))
                if round(distance, 2) > 0:
                    first_index_nectar = 0
                    last_index_nectar = 0
                    first_index_pollen = 0
                    last_index_pollen = 0
                    for index in range(4, 369):
                        if point.record[index] > 0:
                            first_index_nectar = index
                            break
                    for index in range(368, 3, -1):
                        if point.record[index] > 0:
                            last_index_nectar = index
                            break
                    for index in range(369, 734):
                        if point.record[index] > 0:
                            first_index_pollen = index
                            break
                    for index in range(733, 368, -1):
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
                        first_day_flowering = min(first_index_nectar - 1, first_index_pollen - 366)
                        last_day_flowering = max(last_index_nectar - 1, last_index_pollen - 366)
                        nectar = statistics.mean(point.record[first_day_flowering + 1:last_day_flowering + 1])
                        pollen = statistics.mean(point.record[first_day_flowering + 366:last_day_flowering + 366])
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
                            applications = [
                                random.randint(first_day_of_year_applications, last_day_of_year_applications)
                                for _ in range(number_applications)
                            ]
                            applications.sort()
                            conc_nectar = random.normalvariate(conc_nectar_mean, conc_nectar_std)
                            conc_pollen = random.normalvariate(conc_pollen_mean, conc_pollen_std)
                            contact = random.normalvariate(contact_toxicity_mean, contact_toxicity_std)
                            f.write(
                                f"{first_day_flowering}\t{last_day_flowering}\t"
                                f"[{' '.join([str(x) for x in applications])}]\t"
                                f"[{exposure_period}]\t"
                                f"{conc_nectar}\t{conc_pollen}\t{contact}\t"
                                f"10000\t0\t21\n"
                            )
                            for feature in station_patch_mapping.get(point.record["ID"], []):
                                for application in applications:
                                    f2.write(f"{feature},{application},{conc_nectar},{conc_pollen},{contact}\n")
                        else:
                            f.write(f"{first_day_flowering}\t{last_day_flowering}\t[]\t[]\t0\t0\t0\t10000\t0\t0\n")
