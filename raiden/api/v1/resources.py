from webargs.flaskparser import use_kwargs
from flask_restful import Resource
from flask import Blueprint

from raiden.api.v1.encoding import ChannelRequestSchema


def create_blueprint():
    # Take a look at this SO question on hints how to organize versioned
    # API with flask:  http://stackoverflow.com/questions/28795561/support-multiple-api-versions-in-flask#28797512
    return Blueprint('v1_resources', __name__)


class BaseResource(Resource):
    def __init__(self, **kwargs):
        return


class ChannelsResource(BaseResource):

    # define the route of the resource here:
    _route = '/channels'

    # has to be set externally via dependency injection
    rest_api = None
    put_schema = ChannelRequestSchema(
        exclude=('channel_address', 'state'),
    )

    def get(self):
        """
        this translates to 'get all channels the node is connected with'
        """
        return self.rest_api.get_channel_list()

    # e.g. this endpoint will accept the args from all locations:
    # as JSON object, via form data. or as query string
    # change according to what is desired here
    @use_kwargs(put_schema, locations=('json', 'form', 'query'))
    def put(self, **kwargs):
        return self.rest_api.open(**kwargs)


class ChannelsResourceByChannelAddress(Resource):
    _route = '/channels/<hexaddress:channel_address>'
    rest_api = None

    patch_schema = ChannelRequestSchema(
        exclude=('token_address', 'partner_address', 'settle_timeout'),
    )

    @use_kwargs(patch_schema, locations=('json', 'form', 'query'))
    def patch(self, **kwargs):
        # the channel_address kwarg is automatically included in the kwargs,
        # because there is an argument placeholder in the route!
        return self.rest_api.patch_channel(**kwargs)


class TokensResource(BaseResource):
    _route = '/tokens'
    rest_api = None

    patch_schema = ChannelRequestSchema(
        exclude=('channel_address', 'token_address', 'partner_address'),
    )

    def get(self):
        """
        this translates to 'get all token addresses we have channels open for
        """
        # TODO
        pass


class Partner(BaseResource):
    pass


class EventsResoure(BaseResource):
    """
    no args, since we are filtering in the client for now
    """

    _route = '/api/events'
    rest_api = None

    def get(self):
        return self.rest_api.get_new_events()
