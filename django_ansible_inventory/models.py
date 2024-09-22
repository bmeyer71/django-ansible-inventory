from django.db import models
from .fields import LowerCharField, UpperCharField, CommonFields
from netaddr import IPNetwork


def get_default_hosttype():
    try:
        item_default = HostType.objects.get(
            item_default=True,
        )
    except HostType.DoesNotExist:
        return None
    return item_default.pk


def get_default_environment():
    try:
        item_default = Environment.objects.get(
            item_default=True,
        )
    except Environment.DoesNotExist:
        return None
    return item_default.pk


def get_default_purpose():
    try:
        item_default = Purpose.objects.get(
            item_default=True,
        )
    except Purpose.DoesNotExist:
        return None
    return item_default.pk


def get_default_hoststatus():
    try:
        item_default = HostStatus.objects.get(
            item_default=True,
        )
    except HostStatus.DoesNotExist:
        return None
    return item_default.pk


def get_default_hostclass():
    try:
        item_default = HostClass.objects.get(
            item_default=True,
        )
    except HostClass.DoesNotExist:
        return None
    return item_default.pk


class AnsibleGroupTag(models.Model):
    name = UpperCharField(
        max_length=100,
        unique=True,
    )

    class Meta:
        verbose_name = "Ansible Group Tag"
        verbose_name_plural = "Ansible Group Tags"

    def __str__(self):
        return self.name


class AnsibleGroup(models.Model):
    name = LowerCharField(
        max_length=100,
        unique=True,
    )
    tags = models.ManyToManyField(
        AnsibleGroupTag,
        related_name="groups",
        blank=True,
    )
    group_vars = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        verbose_name = "Ansible Group"
        verbose_name_plural = "Ansible Groups"

    def __str__(self):
        return self.name


class NetworkLabel(CommonFields):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Description, e.g., vlan100",
    )
    network = models.CharField(
        max_length=100,
        unique=True,
        help_text="IP network in CIDR notation, e.g., 172.16.0.0/23",
    )

    class Meta:
        verbose_name = "Network Label"
        verbose_name_plural = "Network Labels"

    def __str__(self):
        return self.name

    def get_available_ips(self):
        """
        Returns a list of available IP addresses within the network that are
        not assigned.
        """
        all_ips = IPNetwork(self.network)  # Get all IPs in the network
        assigned_ips = NetworkAddress.objects.filter(
            network_label=self, is_assigned=True
        ).values_list("ip_address", flat=True)

        # Filter out .0 and .255 addresses (commonly reserved) and return only
        # unassigned IPs
        available_ips = [
            str(ip)
            for ip in all_ips
            if str(ip) not in assigned_ips and ip.words[-1] not in [0, 255]
        ]

        return available_ips

    def save(
        self,
        force_insert=False,
        force_update=False,
        *args,
        **kwargs,
    ):
        obj = self.__class__.objects.filter(enabled=True)
        obj_count = obj.count()

        if obj_count == 0:
            self.item_default = True
            self.enabled = True
        elif self.item_default is True:
            for item in obj:
                item.item_default = False
                item.save()

        super(NetworkLabel, self).save(
            force_insert=force_insert,
            force_update=force_update,
            *args,
            **kwargs,
        )


class NetworkAddress(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    network_label = models.ForeignKey(NetworkLabel, on_delete=models.CASCADE)
    is_assigned = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Network Address"
        verbose_name_plural = "Network Addresses"

    def __str__(self):
        return self.ip_address


class HostType(CommonFields):
    host_type = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Host Type"
        verbose_name_plural = "Host Types"

    def __str__(self):
        return self.host_type

    def save(
        self,
        force_insert=False,
        force_update=False,
        *args,
        **kwargs,
    ):
        obj = self.__class__.objects.filter(enabled=True)
        obj_count = obj.count()

        if obj_count == 0:
            self.item_default = True
            self.enabled = True
        elif self.item_default is True:
            for item in obj:
                item.item_default = False
                item.save()

        super(HostType, self).save(
            force_insert=force_insert,
            force_update=force_update,
            *args,
            **kwargs,
        )


class Environment(CommonFields):
    environment = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Environment"
        verbose_name_plural = "Environments"

    def __str__(self):
        return self.environment

    def save(
        self,
        force_insert=False,
        force_update=False,
        *args,
        **kwargs,
    ):
        obj = self.__class__.objects.filter(enabled=True)
        obj_count = obj.count()

        if obj_count == 0:
            self.item_default = True
            self.enabled = True
        elif self.item_default is True:
            for item in obj:
                item.item_default = False
                item.save()

        super(Environment, self).save(
            force_insert=force_insert,
            force_update=force_update,
            *args,
            **kwargs,
        )


class Purpose(CommonFields):
    purpose = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Purpose"
        verbose_name_plural = "Purpose"

    def __str__(self):
        return self.purpose

    def save(
        self,
        force_insert=False,
        force_update=False,
        *args,
        **kwargs,
    ):
        obj = self.__class__.objects.filter(enabled=True)
        obj_count = obj.count()

        if obj_count == 0:
            self.item_default = True
            self.enabled = True
        elif self.item_default is True:
            for item in obj:
                item.item_default = False
                item.save()

        super(Purpose, self).save(
            force_insert=force_insert,
            force_update=force_update,
            *args,
            **kwargs,
        )


class HostStatus(CommonFields):
    host_status = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Host Status"
        verbose_name_plural = "Host Status"

    def __str__(self):
        return self.host_status

    def save(
        self,
        force_insert=False,
        force_update=False,
        *args,
        **kwargs,
    ):
        obj = self.__class__.objects.filter(enabled=True)
        obj_count = obj.count()

        if obj_count == 0:
            self.item_default = True
            self.enabled = True
        elif self.item_default is True:
            for item in obj:
                item.item_default = False
                item.save()

        super(HostStatus, self).save(
            force_insert=force_insert,
            force_update=force_update,
            *args,
            **kwargs,
        )


class HostClass(CommonFields):
    host_class = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Host Class"
        verbose_name_plural = "Host Classes"

    def __str__(self):
        return self.host_class

    def save(
        self,
        force_insert=False,
        force_update=False,
        *args,
        **kwargs,
    ):
        obj = self.__class__.objects.filter(enabled=True)
        obj_count = obj.count()

        if obj_count == 0:
            self.item_default = True
            self.enabled = True
        elif self.item_default is True:
            for item in obj:
                item.item_default = False
                item.save()

        super(HostClass, self).save(
            force_insert=force_insert,
            force_update=force_update,
            *args,
            **kwargs,
        )


class BusinessUnit(CommonFields):
    business_unit = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Business Unit"
        verbose_name_plural = "Business Units"

    def __str__(self):
        return self.business_unit

    def save(
        self,
        force_insert=False,
        force_update=False,
        *args,
        **kwargs,
    ):
        obj = self.__class__.objects.filter(enabled=True)
        obj_count = obj.count()

        if obj_count == 0:
            self.item_default = True
            self.enabled = True
        elif self.item_default is True:
            for item in obj:
                item.item_default = False
                item.save()

        super(BusinessUnit, self).save(
            force_insert=force_insert,
            force_update=force_update,
            *args,
            **kwargs,
        )


class SupportGroup(CommonFields):
    group = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Support Group"
        verbose_name_plural = "Support Groups"

    def __str__(self):
        return self.group

    def save(
        self,
        force_insert=False,
        force_update=False,
        *args,
        **kwargs,
    ):
        obj = self.__class__.objects.filter(enabled=True)
        obj_count = obj.count()

        if obj_count == 0:
            self.item_default = True
            self.enabled = True
        elif self.item_default is True:
            for item in obj:
                item.item_default = False
                item.save()

        super(SupportGroup, self).save(
            force_insert=force_insert,
            force_update=force_update,
            *args,
            **kwargs,
        )


class SupportLevel(CommonFields):
    level = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Support Levels"
        verbose_name_plural = "Support Levels"

    def __str__(self):
        return self.level

    def save(
        self,
        force_insert=False,
        force_update=False,
        *args,
        **kwargs,
    ):
        obj = self.__class__.objects.filter(enabled=True)
        obj_count = obj.count()

        if obj_count == 0:
            self.item_default = True
            self.enabled = True
        elif self.item_default is True:
            for item in obj:
                item.item_default = False
                item.save()

        super(SupportLevel, self).save(
            force_insert=force_insert,
            force_update=force_update,
            *args,
            **kwargs,
        )


class Host(models.Model):
    name = LowerCharField(max_length=255)
    groups = models.ManyToManyField(
        AnsibleGroup,
        related_name="hosts",
    )
    enabled = models.BooleanField(default=True)
    host_vars = models.JSONField(
        default=dict,
        blank=True,
    )
    vlan = models.ForeignKey(
        NetworkLabel,
        on_delete=models.SET_NULL,
        null=True,
    )
    ip_address = models.OneToOneField(
        NetworkAddress,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    short_description = models.CharField(max_length=255)
    host_type = models.ForeignKey(
        HostType,
        on_delete=models.CASCADE,
        default=get_default_hosttype,
        limit_choices_to={
            "enabled": True,
        },
    )
    environment = models.ForeignKey(
        Environment,
        on_delete=models.CASCADE,
        default=get_default_environment,
        limit_choices_to={
            "enabled": True,
        },
    )
    purpose = models.ForeignKey(
        Purpose,
        on_delete=models.CASCADE,
        default=get_default_purpose,
        limit_choices_to={
            "enabled": True,
        },
    )
    host_status = models.ForeignKey(
        HostStatus,
        on_delete=models.CASCADE,
        default=get_default_hoststatus,
        limit_choices_to={
            "enabled": True,
        },
    )
    host_class = models.ForeignKey(
        HostClass,
        on_delete=models.CASCADE,
        default=get_default_hostclass,
        limit_choices_to={
            "enabled": True,
        },
    )
    business_unit = models.ForeignKey(
        BusinessUnit,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    support_group = models.ForeignKey(
        SupportGroup,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    support_level = models.ForeignKey(
        SupportLevel,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Host"
        verbose_name_plural = "Hosts"

    def __str__(self):
        return self.name
