from rest_framework.renderers import BrowsableAPIRenderer


class StaffBrowsableAPIRenderer(BrowsableAPIRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        ret = ''
        if renderer_context:
            if renderer_context.get('request'):
                if renderer_context['request'].user.is_staff:
                    ret = super(StaffBrowsableAPIRenderer, self).render(
                        data, accepted_media_type=accepted_media_type, renderer_context=renderer_context
                    )
        return ret
