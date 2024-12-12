class ApiResponse:
	@staticmethod
	def success_response(message, statuscode, data):

		success_res = {
			'statusCode':statuscode,
			'statusMessage':message,
			'responseObject':data
		}

		return success_res

	@staticmethod
	def error_response(error, statuscode):
		error_res = {
			'statusCode':statuscode,
			'statusMessage':str(error),
			'errors':repr(error)
		}

		return error_res