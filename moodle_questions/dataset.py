class dataset_definition:
    """
    This class defines the name, type, distribution etc of the
    dataset along with max, min, itemcount etc.

    There is also a method to generate itemcount dataset_items
    for each variable specified.

    The user has to make sure that the names of these variables
    are the same as the moodle formula prescribed.
    """

    def __init__(self, variable, itemcount, dist, minimum, maximum, decimals):
        self.itemcount = itemcount
        self.minimum = minimum
        self.maximum = maximum
        self.distribution = dist
        self.variable = variable
        self.decimals = decimals

    def _to_xml_element(self, st="private"):
        dataset = et.Element("dataset_definition")
        status = et.SubElement(dataset, "status")
        text = et.SubElement(status, "text")
        text.text = st   # shared or private 

        name = et.SubElement(dataset, "name")
        text = et.SubElement(name, "text")
        text.text = self.variable

        #type=calculated?

        distribution = et.SubElement(dataset, "distribution")
        text = et.SubElement(distribution, "text")
        text.text = self.distribution

        minimum = et.SubElement(dataset, "minimum")
        text = et.SubElement(minimum, "text")
        text.text = str(self.minimum)

        maximum = et.SubElement(dataset, "maximum")
        text = et.SubElement(maximum, "text")
        text.text = str(self.maximum)

        decimals = et.SubElement(dataset, "decimals")
        text = et.SubElement(decimals, "text")
        text.text = str(self.decimals)

        itemcount = et.SubElement(dataset, "itemcount")
        itemcount.text = str(self.itemcount)

        dataset_items = et.SubElement(dataset, "dataset_items")

        for i in range(1, self.itemcount+1):
            dataset_item = et.SubElement(dataset_items, "dataset_item")
            number = et.SubElement(dataset_item, "number")
            number.text = str(i)

            value = et.SubElement(dataset_item, "value")
            value.text = str(round(uniform(self.minimum, self.maximum), self.decimals))

        number_of_items = et.SubElement(dataset, "number_of_items")
        number_of_items.text = str(self.itemcount)

        return dataset            
